from rest_framework import serializers
from posts.models import Post, Comment, Group, Follow


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'id')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username', default=serializers.CurrentUserDefault)
    following = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(queryset=model.objects.all(), fields=('user', 'following'),
                                                message='The subscription already exists')
        ]
