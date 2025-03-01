from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# app_name = 'indianews'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('video/<str:video_data>/', views.openVideoPage, name='video_page'),
    path('video/', views.openVideoPage, name='video_search'), 
    path('videoupload/', views.videoUpload, name='video_upload'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)