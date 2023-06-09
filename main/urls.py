"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blogs/', include('blogs.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import HomeView
from apps.blogs.views import BlogView, AddBlogView, DetailBlogView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', HomeView.as_view(), name='signup_page'),
    path('home/', BlogView.as_view(), name='home'),
    path('add_blog/', AddBlogView.as_view(), name='add_blog'),
    path('blog_detail/', DetailBlogView.as_view(), name='blog_detail'),
    path('users/', include('apps.users.urls')),
    path('blogs/', include('apps.blogs.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)