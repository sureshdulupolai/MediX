from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('short-upload/', views.shortUpload, name='shorts_upload'),
    path('short/<int:st_id>/', views.callVideo, name='shorts_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)