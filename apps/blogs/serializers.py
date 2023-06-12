from rest_framework import serializers
from .models import BlogModel
from .models import Comment, Like

"""
The CommentSerializer class is defined for serializing the Comment model.
The name field is added using SerializerMethodField(), which will call the get_name method to retrieve the name of the user associated with the comment.
The Meta class specifies the model as Comment and lists the desired fields to include in the serialized representation.
"""
class CommentSerializer(serializers.ModelSerializer):
    # blog_id = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'blog', 'user_email','user_image']

    def get_user_email(self, comment):
        return comment.user.email

    def get_user_image(self, comment):
        return comment.blog.image.url if comment.blog.image else None




"""
The LikeSerializer class is defined for serializing the Like model.
The Meta class specifies the model as Like and includes all fields ('__all__') in the serialized representation.
"""
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


"""
The BlogSerializer class is defined for serializing the BlogModel.
It includes nested serializers for Comment and Like models using CommentSerializer and LikeSerializer respectively.
The Meta class specifies the model as BlogModel and includes all fields ('__all__') in the serialized representation.
The validate_title method is used to validate the title field of the BlogModel. 
It checks if the length of the title is greater than 1000 characters and raises a serializers.ValidationError if it is.
The validate_content method is used to validate the content field of the BlogModel. 
It checks if the length of the content is less than 10 characters and raises a serializers.ValidationError if it is.
"""
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




