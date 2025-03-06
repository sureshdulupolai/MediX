from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# app_name = 'indianews'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('video/<str:video_data>/', views.openVideoPage, name='video_page'),
    path('video/', views.searchPage, name='video_search'), 
    path('videoupload/', views.videoUpload, name='video_upload'),
    path('search-page/', views.openVideoPage, name='search_page'),
    path('check-video/', views.CheckVideoPage),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)