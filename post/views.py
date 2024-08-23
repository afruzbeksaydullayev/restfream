from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from post.serializer import PostSerializer
from post.models import Post
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
# Create your views here.



class PostApiView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.select_related('author').prefetch_related('tags')
        return queryset 
    #@method_decorator(cache_page(60 * 2))
    def get(self, request, *args, **kwargs):
        cache_key = 'post_list'
        posts = cache.get(cache_key)
        if posts is None:
            posts = Post.objects.all()
            results = self.paginate_queryset(posts, request, view=self)

            serializer = PostSerializer(results, many=True)
            cache.set(cache_key, serializer.data, timeout=60*5)
            return self.get_paginated_response(serializer.data)
        return Response(posts)
        
    
class PostModelSet(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
        

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': True,
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class PostDetailApiView(APIView):
    def put(self,request, pk):
        post = Post.objects.get(id = pk)
        serializer = PostSerializer(post, data= request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        

    def patch(self):
        pass 

    def delete(self):
        pass

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        cache_key =f'post_detail_{post_id}'
        post = cache.get(cache_key)
        if not post:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post, many=False)
            cache.set(cache_key, serializer.data,timeout=60*3)
            return Response(serializer.data)
        return Response(post)
         
        if not post:
        # Agar post keshda mavjud bo'lmasa, uni DB dan yoki boshqa joydan oling
            post = Post.objects.all()  # Misol uchun: barcha postlarni olish
            cache.set(cache_key, post, timeout=60*15)  # 15 daqiqaga keshga yozish
    
        return Response(post)
    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    