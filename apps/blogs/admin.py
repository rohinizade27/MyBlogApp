from django.contrib import admin
from .models import BlogModel,Comment,Like

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','content','image','created_at','upload_to')


admin.site.register(BlogModel, BlogAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user','blog','content')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)