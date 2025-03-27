from .models import ShortsDetails
from django import forms

class ShortsForm(forms.ModelForm):
    class Meta:
        model = ShortsDetails
        fields = ['short_title', 'short_thumbnail', 'short_link', 'short_description']

