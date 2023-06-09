from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BlogModel, Comment, Like, CustomUser
from .serializers import BlogSerializer, CommentSerializer, LikeSerializer
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView
from rest_framework.permissions import BasePermission
from rest_framework.permissions import AllowAny


class BlogView(TemplateView):
    template_name = 'blog/home.html'

class AddBlogView(TemplateView):
    template_name = 'blog/add_blog.html'

class DetailBlogView(TemplateView):
    template_name = 'blog/blog_detail.html'


def logout_view(request):
    logout(request)
    return redirect('/')

class BlogListCreateAPIView(APIView):

    class AllowAnyPermission(BasePermission):
        def has_permission(self, request, view):
            # Allow any user to access this method
            return True

    permission_classes = [AllowAnyPermission]

    def get(self, request):
        request.data['user'] = request.user.id
        print('user -->', request.user.id, request.data)
        blogs = BlogModel.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        data = serializer.data
        for item in data:
            blog_id = item['id']
            user = item['user']
            try:
                user = CustomUser.objects.get(id=user)
                email = user.email
            except:
                email = None
            blog = BlogModel.objects.get(id=blog_id)
            likes = Like.objects.filter(blog_id=blog_id)
            like_count = likes.count()
            # item['created_by'] = blog.user.name
            item['comments'] = CommentSerializer(blog.comments.all(), many=True).data
            item['like_count'] = like_count
            item['user'] = email

        return Response(data)

    def post(self, request):
        request.data['user'] = request.user.id
        print('user -->', request.user.id, request.data)
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogRetrieveUpdateDestroyAPIView(APIView):
    class AllowAnyPermission(BasePermission):
        def has_permission(self, request, view):
            # Allow any user to access this method
            return True

    permission_classes = [AllowAnyPermission]

    def get_object(self, pk):
        try:
            return BlogModel.objects.get(pk=pk)
        except BlogModel.DoesNotExist:
            return None

    def get(self, request, pk):
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog)
        data = serializer.data
        blog_id = data['id']
        user = data['user']
        try:
            user = CustomUser.objects.get(id=user)
            email = user.email
        except:
            email = None
        blog = BlogModel.objects.get(id=blog_id)
        likes = Like.objects.filter(blog_id=blog_id)
        like_count = likes.count()
        print(email)
        # item['created_by'] = blog.user.name
        data['comments'] = CommentSerializer(blog.comments.all(), many=True).data
        data['like_count'] = like_count
        data['user'] = email
        return Response(data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlogSearchAPIView(APIView):
    def get(self, request):
        search_query = request.query_params.get('query', '')
        blogs = BlogModel.objects.filter(title__icontains=search_query)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)


class CommentListCreateAPIView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeListCreateAPIView(APIView):
    def get(self, request):
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogListByUserAPIView(APIView):
    def get_object(self, pk):
        try:
            return BlogModel.objects.get(pk=pk)
        except BlogModel.DoesNotExist:
            return None

    def get(self, request, pk):
        user_id = request.user.pk
        blogs = BlogModel.objects.filter(user_id=user_id)
        serializer = BlogSerializer(blogs, many=True)
        data = serializer.data
        for item in data:
            blog_id = item['id']
            user = item['user']
            try:
                user = CustomUser.objects.get(id=user)
                email = user.email
            except:
                email = None
            blog = BlogModel.objects.get(id=blog_id)
            likes = Like.objects.filter(blog_id=blog_id)
            like_count = likes.count()
            # item['created_by'] = blog.user.name
            item['comments'] = CommentSerializer(blog.comments.all(), many=True).data
            item['like_count'] = like_count
            item['user'] = email

        return Response(data)
        # serializer = BlogSerializer(blogs, many=True)
        # data = serializer.data
        # for item in blogs:
        #         blog = BlogModel.objects.get(id=item.id)
        #         item['user']: blog.user.email
        #         item['comments']: CommentSerializer(blog.comments.all(), many=True).data
        #         item['like_count']: Like.objects.filter(blog_id=blog.id).count()
        # return Response(data)