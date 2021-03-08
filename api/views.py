from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from .models import Post, Comment
from .serializers import (
    PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
)
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.select_related('post', 'author').all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    pass


class GroupViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    pass
