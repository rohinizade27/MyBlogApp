from django.contrib import admin
from .models import CustomUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','name','is_staff', 'is_active', 'date_joined')


admin.site.register(CustomUser, UserAdmin)


