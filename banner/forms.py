from django import forms
from .models import BannerDetails

class bannerForm(forms.ModelForm):
    class Meta:
        model = BannerDetails
        fields = ['banner_img', 'banner_title', 'contact_no']