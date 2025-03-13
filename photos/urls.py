from django.urls import path
from . import views

urlpatterns = [
    path('upload-photo', views.uploadPhoto, name='upload_photo'),
]