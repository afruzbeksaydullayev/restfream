from rest_framework.generics import RetrieveAPIView
from app.models import Product, Attribute
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serialaizer import ProductSerializer, CommentSerializer, AttributeSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.permissions import CustomPermissions


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermissions]
    
    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        group_slug = self.kwargs['group_slug']
        queryset = Product.objects.filter(group__category__slug = category_slug, group__slug = group_slug).select_related('proup').prefetch_related('comment')
        
        return queryset

    
    
class ProductCreatedApiView(APIView):
    
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Product successfully created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDeleteApiView(APIView):
    def get(self, request, slug):
        product = Product.objects.get(slug = slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self,slug):
        product = Product.objects.get(slug = slug)

        if product:
            product.delete()
            data = {
                'data': 'Product successfuly deleted',
                'status': status.HTTP_200_OK
            }
            return Response(data)
        
class ProductUpdateApiView(APIView):
    def get(self,request, slug):
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, slug):
        product = Product.objects.get(slug = slug)
        serializer = ProductSerializer(data = request.data, isinstance = product)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message':'Update successfully',    
                'status': status.HTTP_200_OK
            }
            return Response(data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class ProductDetailApiView(RetrieveAPIView):
    permission_classes = [CustomPermissions]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


    
