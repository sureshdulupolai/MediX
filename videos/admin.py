from django.contrib import admin
from .models import VideoDetails, VideoCategory

# Register your models here.
class VideoDetailsAdmin(admin.ModelAdmin):
     # Display these fields in the admin list view
    list_display = ('video_title', 'created_date', 'view')
    list_editable = ('view',)  # Enable editing for video_title in the list view

admin.site.register(VideoDetails, VideoDetailsAdmin)
admin.site.register(VideoCategory)