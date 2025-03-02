from django.shortcuts import render

# Create your views here.
def bannerPage(request):
    return render(request, 'bannerUpload.html')