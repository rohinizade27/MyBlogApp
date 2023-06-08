from rest_framework import serializers
from .models import BlogModel
from .models import Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'name', 'blog', 'content', 'created_at']

    def get_name(self, obj):
        return obj.user.name

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = BlogModel
        fields = '__all__'


    def validate_title(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError("Title must be less than or equal to 1000 characters.")
        return value

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value




