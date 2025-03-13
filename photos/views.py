from django.shortcuts import render

# Create your views here.
def uploadPhoto(request):
    return render(request, 'photos-upload.html')