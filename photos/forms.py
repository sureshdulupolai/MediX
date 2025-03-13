from django import forms
from .models import Post, PostImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']

class PostWithImagesForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'images']