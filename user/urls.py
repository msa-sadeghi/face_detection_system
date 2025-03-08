from django.urls import path
from . import views
from django.contrib import admin
admin.site.site_header = 'مدیریت سامانه'
admin.site.index_title = 'مدیریت سامانه'
admin.site.site_title = 'مدیریت سامانه'
app_name = "user"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
