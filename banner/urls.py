from django.urls import path
from . import views

urlpatterns = [
    path('banner-upload/', views.bannerPage, name='banner'),
]