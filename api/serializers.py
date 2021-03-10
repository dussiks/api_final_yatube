from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Post, Follow, Group, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='username'
    )
    group = serializers.ReadOnlyField(source='group.title')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following']
        )]

    def validate(self, data):
        request = self.context['request']
        if request.user == data.get('following'):
            raise serializers.ValidationError(
                'User can not follow himself.'
            )
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title',)
        model = Group
