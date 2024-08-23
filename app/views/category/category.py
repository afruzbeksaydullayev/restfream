from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response
from app.models import  Category
from app.serialaizer import CategorySerializer
from rest_framework import generics
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView


'''class CategiryApiView(APIView):
    
    def get(self, request):
        category_data = [{
            'title': category.title,
            'image': category.image.url if category.image else None,

        }
        for category in Category.objects.all()]     
        return Response (category_data, status=status.HTTP_200_OK)'''

class CategoryListApiView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


'''class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer '''
    
class CategoryDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return generics.get_object_or_404(Category, slug=slug)

'''class CategoryDetailApiView(APIView):
    def get(self,request,slug):
        category = Category.objects.get( slug = slug)
        serialazer = CategorySerializer(category)
        return Response(serialazer.data, status=status.HTTP_200_OK)'''


'''class CategoryDetailApiView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'''

'''class CategoryCreatedApiView(APIView):

    def post(self, request):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Product successfully created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''


class CategoryCreatedApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    
'''class CategoryUpdateApiView(APIView):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def post(self, request, slug):
        category=Category.objects.get(slug=slug)
        serializer = CategorySerializer(data=request.data, instance= category)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message':'Update successfully',
                'status': status.HTTP_200_OK
            }
            return Response(data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''

class CategoryUpdateApiView(RetrieveUpdateAPIView):   
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


'''class CategoryDeleteApiView(APIView):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def delete(self, request, slug):
        category = Category.objects.get(slug=slug)
        if category:
            category.delete()
            data = {
                'data': 'Category successfuly deleted',
                'status': status.HTTP_200_OK
            }
            return Response(data)'''

class CategoryDeleteApiView(RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'