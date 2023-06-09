from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BlogModel, Comment, Like, CustomUser
from .serializers import BlogSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import BasePermission

"""
The BlogView class is a view that extends TemplateView.
It renders the blog/home.html template.
"""
class BlogView(TemplateView):
    template_name = 'blog/home.html'


"""
The AddBlogView class is a view that extends TemplateView.
It renders the blog/add_blog.html template.
"""
class AddBlogView(TemplateView):
    template_name = 'blog/add_blog.html'


"""
The DetailBlogView class is a view that extends TemplateView.
It renders the blog/blog_detail.html template.
"""
class DetailBlogView(TemplateView):
    template_name = 'blog/blog_detail.html'


"""
The BlogListCreateAPIView class is an API view.
It extends APIView from Django REST Framework.
The AllowAnyPermission class is a custom permission class that allows any user to access the methods.
The get() method retrieves all blog objects from the database, serializes them using BlogSerializer, 
and returns the serialized data in the response.
The post() method creates a new blog object based on the request data, validates it using BlogSerializer, 
and saves it to the database if valid. It returns the serialized data of the created blog in the response
"""
class BlogListCreateAPIView(APIView):
    # Custom permission class that allows any user to access this method
    class AllowAnyPermission(BasePermission):
        def has_permission(self, request, view):
            # Allow any user to access this method
            return True

    permission_classes = [AllowAnyPermission]

    def get(self, request):
        # Assign the user ID to the request data
        request.data['user'] = request.user.id
        # Retrieve all blog objects from the database
        blogs = BlogModel.objects.all()
        # Serialize the blog objects
        serializer = BlogSerializer(blogs, many=True)
        data = serializer.data
        for item in data:
            # Extract the blog ID and user ID from the serialized data
            blog_id = item['id']
            user = item['user']
            try:
                # Retrieve the CustomUser object using the user ID
                user = CustomUser.objects.get(id=user)
                email = user.email
            except:
                # If the user is not found, set the email to None
                email = None
            # Retrieve the BlogModel object using the blog ID
            blog = BlogModel.objects.get(id=blog_id)
            # Retrieve all the likes associated with the blog
            likes = Like.objects.filter(blog_id=blog_id)
            like_count = likes.count()
            # Serialize and include the comments associated with the blog
            item['comments'] = CommentSerializer(blog.comments.all(), many=True).data
            item['like_count'] = like_count
            item['user'] = email

        return Response(data)

    def post(self, request):
        # Assign the user ID to the request data
        request.data['user'] = request.user.id
        print('user -->', request.user.id, request.data)
        # Serialize the request data
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            # Save the serialized data as a new BlogModel object
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
The BlogRetrieveUpdateDestroyAPIView class is an API view.
It extends APIView from Django REST Framework.
The AllowAnyPermission class is a custom permission class that allows any user to access the methods.
The get_object() method retrieves a blog object based on the given primary key.
The get() method retrieves a specific blog object, serializes it using BlogSerializer, 
and returns the serialized data in the response.
The put() method updates a specific blog object with the request data, 
validates it using BlogSerializer, and returns the updated serialized data in the response.
The patch() method partially updates a specific blog object with the request data, 
validates it using BlogSerializer, and returns the updated serialized data in the response.
The delete() method deletes a specific blog object and returns a response with no content.
"""
class BlogRetrieveUpdateDestroyAPIView(APIView):
    class AllowAnyPermission(BasePermission):
        def has_permission(self, request, view):
            # Allow any user to access this method
            return True

    permission_classes = [AllowAnyPermission]

    def get_object(self, pk):
        try:
            # Retrieve the BlogModel object using the given primary key
            return BlogModel.objects.get(pk=pk)
        except BlogModel.DoesNotExist:
            return None

    def get(self, request, pk):
        # Retrieve the BlogModel object
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog)
        data = serializer.data
        blog_id = data['id']
        user = data['user']
        try:
            # Retrieve the CustomUser object using the user ID
            user = CustomUser.objects.get(id=user)
            email = user.email
        except:
            email = None
        blog = BlogModel.objects.get(id=blog_id)
        likes = Like.objects.filter(blog_id=blog_id)
        like_count = likes.count()
        print(email)
        # Serialize and include the comments associated with the blog
        data['comments'] = CommentSerializer(blog.comments.all(), many=True).data
        data['like_count'] = like_count
        data['user'] = email
        return Response(data)

    def put(self, request, pk):
        # Retrieve the BlogModel object
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Serialize the request data and update the BlogModel object
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Retrieve the BlogModel object
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Serialize the request data and update the BlogModel object partially
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Retrieve the BlogModel object
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Delete the BlogModel object
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
The BlogSearchAPIView class is an API view.
It extends APIView from Django REST Framework.
The get() method retrieves the search query parameter from the request and 
filters blog objects based on the title containing the search query. 
It serializes the filtered blog objects using BlogSerializer 
and returns the serialized data in the response.
"""
class BlogSearchAPIView(APIView):
    def get(self, request):
        # Retrieve the search query parameter from the request
        search_query = request.query_params.get('query', '')
        # Filter blog objects based on the title containing the search query
        blogs = BlogModel.objects.filter(title__icontains=search_query)
        # Serialize the filtered blog objects
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)


"""
The CommentListCreateAPIView class is an API view.
It extends APIView from Django REST Framework.
The get() method retrieves all comment objects from the database, 
serializes them using CommentSerializer, and returns the serialized data in the response.
The post() method creates a new comment object based on the request data, 
validates it using CommentSerializer, and saves it to the database if valid. 
It returns the serialized data of the created comment in the response.
"""
class CommentListCreateAPIView(APIView):
    def get(self, request):
        # Retrieve all comment objects from the database
        comments = Comment.objects.all()
        # Serialize the comment objects
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Serialize the request data
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Save the serialized data as a new Comment object
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
The LikeListCreateAPIView class is an API view.
It extends APIView from Django REST Framework.
The get() method retrieves all like objects from the database, 
serializes them using LikeSerializer, and returns the serialized data in the response.
The post() method creates a new like object based on the request data, 
validates it using LikeSerializer, and saves it to the database if valid. 
It returns the serialized data of the created like in the response.
"""
class LikeListCreateAPIView(APIView):
    def get(self, request):
        # Retrieve all like objects from the database
        likes = Like.objects.all()
        # Serialize the like objects
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Serialize the request data
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            # Save the serialized data as a new Like object
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
The BlogListByUserAPIView class is an API view.
It extends APIView from Django REST Framework.
The get_object() method retrieves a blog object based on the given primary key.
The get() method retrieves blog objects filtered by the user ID of the current user, 
serializes them using BlogSerializer, and returns the serialized data in the response. 
It also includes comments and like counts associated with each blog in the response.
"""
class BlogListByUserAPIView(APIView):
    def get_object(self, pk):
        try:
            # Retrieve the BlogModel object using the given primary key
            return BlogModel.objects.get(pk=pk)
        except BlogModel.DoesNotExist:
            return None

    def get(self, request, pk):
        # Retrieve the user ID of the current user
        user_id = request.user.pk
        # Filter blog objects based on the user ID
        blogs = BlogModel.objects.filter(user_id=user_id)
        # Serialize the filtered blog objects
        serializer = BlogSerializer(blogs, many=True)
        data = serializer.data
        for item in data:
            # Extract the blog ID and user ID from the serialized data
            blog_id = item['id']
            user = item['user']
            try:
                # Retrieve the CustomUser object using the user ID
                user = CustomUser.objects.get(id=user)
                email = user.email
            except:
                email = None
            # Retrieve the BlogModel object using the blog ID
            blog = BlogModel.objects.get(id=blog_id)
            # Retrieve all the likes associated with the blog
            likes = Like.objects.filter(blog_id=blog_id)
            like_count = likes.count()
            # Serialize and include the comments associated with the blog
            item['comments'] = CommentSerializer(blog.comments.all(), many=True).data
            item['like_count'] = like_count
            item['user'] = email

        return Response(data)

