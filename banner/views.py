from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import bannerForm
from.models import BannerDetails


# Create your views here.
def bannerPage(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            messages.info(request, "The price to upload a banner is $2")
        if request.method == 'POST':
            banner_img = request.FILES.get('banner_img')
            banner_title = request.POST.get('banner_title')
            contact_no = request.POST.get('contact_no')

            obj = BannerDetails(
                banner_img = banner_img,
                banner_title = banner_title,
                contact_no = contact_no,
                uName = request.user
            )

            obj.save()
            return redirect('profile')

        return render(request, 'bannerUpload.html')
    
    else:
        return redirect('login')
