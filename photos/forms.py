from django import forms
from .models import Post, PostImage  # Import your models

class PostWithImagesForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),  # ✅ Corrected Widget
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content']