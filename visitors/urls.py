from django.urls import path
from . import views
app_name = "visitors"
urlpatterns = [
    path('register/', views.register_visitor, name='register'),
    path('', views.identify_visitor, name='identify'),
]
