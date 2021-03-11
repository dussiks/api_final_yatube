from rest_framework import viewsets, permissions, mixins
from rest_framework.generics import get_object_or_404

from .models import Post, Follow, Group, User
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
    serializer_class = PostSerializer
    queryset = Post.objects.optimized()
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        queryset = post.comments.filter(post=post.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    search_fields = ['user__username']

    def get_queryset(self):
        following = get_object_or_404(
            User, username=self.request.user.username
        )
        queryset = following.following.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(CreateListViewSet):
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Group.objects.all()
