from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    site_title = "مدیریت مراجعه کنندگاه"
    site_header  = "مدیریت مراجعه کنندگاه"
    index_title  = "مدیریت مراجعه کنندگاه"
    model = CustomUser
    list_display = ('username', 'email', 'is_manager', 'is_staff')
    list_filter = ('is_manager', 'is_staff')
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
