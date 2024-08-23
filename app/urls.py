from django.urls import path

from app.views.category.category import  CategoryListApiView, CategoryDetailApiView, CategoryCreatedApiView, CategoryUpdateApiView, CategoryDeleteApiView

from app.views.group.groups import GroupListApiView, GroupCreateApiview, GroupDetailApi

from app.views.product.product_view import ProductListApiView, ProductCreatedApiView, ProductDetailApiView, ProductDeleteApiView, ProductUpdateApiView

from app.views.auth.auth_view import UserLoginAPIView, UserLogoutAPIView, UserRegisterAPIView
urlpatterns = [

    #category
    path('category/', CategoryListApiView.as_view(), name='category-list'),
    path('category/<slug:slug>/detail/', CategoryDetailApiView.as_view(), name='category-detail'),
    path('category/create/', CategoryCreatedApiView.as_view(), name='category-create'),
    path('category/<slug:slug>/edit/', CategoryUpdateApiView.as_view()),
    path('category/<slug:slug>/delete/', CategoryDeleteApiView.as_view()),

    #Group
    path('category/<slug:slug>/', GroupListApiView.as_view(), name='group-list'),
    path('group/create/', GroupCreateApiview.as_view(), name='group-create'),
    path('group/<slug:slug>/detail/', GroupDetailApi.as_view(), name='group-detail'),

    #Product
    path('category/<slug:category_slug>/<slug:group_slug>/', ProductListApiView.as_view(), name='product-list'),
    path('product/create/', ProductCreatedApiView.as_view(), name='product-create'),
    path('product/<slug:slug>/delete/', ProductDeleteApiView.as_view()),
    path('product/<slug:slug>/edit/', ProductUpdateApiView.as_view()),

    path('product/view/<slug:slug>/',ProductDetailApiView.as_view()),


    path('login/', UserLoginAPIView.as_view()),
    path('logout/', UserLogoutAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),



 


]