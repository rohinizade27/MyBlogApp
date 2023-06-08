from .views import *
from django.urls import path

urlpatterns = [
    path('home/', BlogView.as_view(), name='home'),
    path('api/blog-list-create/', BlogListCreateAPIView.as_view(), name='blog-list-create'),
    path('api/blog-retrieve-update-destroy/<int:pk>/', BlogRetrieveUpdateDestroyAPIView.as_view(), name='blog-retrieve-update-destroy'),
    path('api/blog-search/', BlogSearchAPIView.as_view(), name='blog-search'),
    path('api/comment-list-create/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('api/like-list-create/', LikeListCreateAPIView.as_view(), name='like-list-create'),

]

