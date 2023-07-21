from rest_framework import serializers
from django.conf import settings
from models import Post, Comment
 
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'created_date', 'published_date']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'author', 'text', 'created_date', 'approved_comment']