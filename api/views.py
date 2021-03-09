from rest_framework import viewsets, permissions, mixins
from rest_framework.generics import get_object_or_404

from .models import Post, Comment, Follow, Group
from .serializers import (
    PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
)
from .permissions import IsOwnerOrReadOnly


class CreateListViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


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


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        queryset = Follow.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(CreateListViewSet):
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Group.objects.all()
