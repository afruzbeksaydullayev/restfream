from django.urls import path
from post.views import PostApiView, PostModelSet, PostDetailApiView, PostViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('post', PostViewSet, basename='post')
urlpatterns=[
    path('post-list/',PostApiView.as_view()),
    path('post-action/',PostModelSet.as_view()),
    path('post-detail/<int:pk>/',PostDetailApiView.as_view()),

]+ router.urls