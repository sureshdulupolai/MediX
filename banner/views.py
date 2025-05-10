from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import bannerForm
from.models import BannerDetails, BannerUploadUnSuccess
from django.http import JsonResponse


# Create your views here.
def bannerPage(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            messages.info(request, "The price to upload a banner is $2")
        if request.method == 'POST':
            banner_img = request.FILES.get('banner_img')
            banner_title = request.POST.get('banner_title')
            contact_no = request.POST.get('contact_no')

            obj = BannerUploadUnSuccess(
                banner_Images = banner_img,
                banner_t = banner_title,
                contact_no = contact_no,
                UserName = request.user
            )

            obj.save()
            ObjId = obj.id
            Usernames = request.user.username

            return redirect('bannerPayment', ObjId=ObjId, Usernames=Usernames)

        return render(request, 'bannerUpload.html')
    
    else:
        return redirect('login')

def bannerPayment(request, ObjId, Usernames):
    if request.method == 'POST':
        return redirect('on_approve')
    
    context = {
        'ObjId' : ObjId,
        'Usernames' : Usernames
    }
    return render(request, 'payNow.html', context)

def On_Approve_View(request):
    context = {}
    return JsonResponse(context)

def Payment_Success_View(request, ObjId, Usernames):
    BUUS = BannerUploadUnSuccess.objects.get(id = ObjId)
    image = BUUS.banner_Images; title = BUUS.banner_t; mobileNo = BUUS.contact_no; userName = BUUS.UserName
    BD = BannerDetails(
        banner_img = image,
        banner_title = title,
        contact_no = mobileNo,
        uName = userName
    )

    BD.save()
    BUUS.delete()
    return redirect('profile')