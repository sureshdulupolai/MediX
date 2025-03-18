from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# app_name = 'indianews'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('video/<int:video_data>/', views.openVideoPage, name='video_page'),
    path('search-page/', views.searchPage, name='video_search'), 
    path('videoupload/', views.videoUpload, name='video_upload'),
    path('search-page/', views.openVideoPage, name='search_page'),
    path('conformation/<str:video_title>/', views.videoDelete, name='delete_video'),
    path('successfully-deleted/<str:video_title>/', views.successfullydeleted,name='data_video_deleted'),
    path('edit-video/<int:item_id>/', views.updateVideo, name='edit_video'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    