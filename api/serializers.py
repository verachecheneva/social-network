from rest_framework import serializers
from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
