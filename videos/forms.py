from django import forms
from .models import VideoDetails

class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoDetails
        fields = ['video_thumbnail', 'video_title', 'video_link', 'video_description', 'video_aim', 'customer_name']
