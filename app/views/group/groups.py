from rest_framework import generics
from app.models import Group
from app.serialaizer import GroupSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser


class GroupListApiView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Group.objects.select_related('category')
        return queryset

class GroupCreateApiview(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return generics.get_object_or_404(Group, slug=slug)