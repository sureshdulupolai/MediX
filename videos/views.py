from django.shortcuts import render, redirect
from .models import VideoDetails, VideoCategory
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import VideoForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from shorts.models import ShortsDetails
from banner.models import BannerDetails
from users.models import ProfileDetails
from django.db.models import Q
import random

def short():
    short = ShortsDetails.objects.all().values()
    return short

def callVideo():
    return VideoDetails.objects.all().values()

def homepage(request):
    ban = list(BannerDetails.objects.all().values())
    val = callVideo()  # Already converted to list
    shorts = list(short())  # Ensure this is a list
    val1 = []
    for i in val:
        title = i['video_title']
        if len(title) >= 32:
            val1 += [i]
        else:
            continue

    # print(val1)
    random.shuffle(val1)
    random.shuffle(shorts)
    random.shuffle(ban)

    # print(val)

    context = {
        'video': val1,
        'shorts': shorts,
        'banner': ban,
    }
    return render(request, 'homepage.html', context)


def openVideoPage(request, video_data=None):
    req = request
    video = None
    other_videos = VideoDetails.objects.all()

    if video_data:
        if video_data.isdigit():
            video = VideoDetails.objects.filter(id=video_data).first()
        else: 
            video = VideoDetails.objects.filter(
                Q(video_title__icontains=video_data) |
                Q(customer_name__username__icontains=video_data) |
                Q(video_description__icontains=video_data)
            ).first()

        if video:
            # Removing the currently playing video from the list
            other_videos = list(other_videos.exclude(id=video.id))
            random.shuffle(other_videos)

    context = {"video": video, "other_videos": other_videos, 'req': req}  
    return render(request, 'Open-Video.html', context)

def searchPage(request):
    if request.method == 'POST' and 'videoName' in request.POST:
        data = request.POST['videoName']
        video_data = request.POST['videoName']
        print(video_data)
        if video_data.isdigit():  
            video = VideoDetails.objects.filter(id=video_data).first()
        else:
            video = VideoDetails.objects.filter(video_title__icontains=video_data) | \
                    VideoDetails.objects.filter(video_description__icontains=video_data)
            # print('v2', video)
    
    val = list(video)
    context = {
        'video': val,
        'data' : data,
    }
    return render(request, 'searchPage.html', context)

@csrf_exempt
def videoUpload(request):
    if request.user.is_authenticated:
        form = VideoForm()
        if request.method == 'POST':
            form = VideoForm(request.POST,  request.FILES)
            if form.is_valid():
                messages.success( 
                    request, 'Your video uploaded successfully to system'
                )
                form.save()
                return redirect('video_upload')

        context = {'form': form}
        return render(request, 'video-upload.html', context)

    else:
        return redirect ('login')
 
def CheckVideoPage(request):
    val = VideoCategory.objects.values_list('vd_category', flat=True)

    category = list(set(val))
    for x1 in category:
        for x2 in category:
            if x1 < x2:
                x1, x2 = x2, x1

    cat = list(category)

    random.shuffle(cat)

    context = {
        'category' :  cat,
    }
    return render(request, 'check-videopage.html', context)

# def CheckVideoPage(request):
#     lst = []
#     val = VideoCategory.objects.all().values()
#     val1 = list(val)

#     for i in val1:
#         lst += (i['vd_category'], )
#     category = set(lst)
    
#     for x1 in category:
#         for x2 in category:
#             if x1 < x2:
#                 x1, x2 = x2, x1

#     cat = list(category)
    
#     random.shuffle(cat)
#     context = {
#         'category' :  cat,
#     }
#     return render(request, 'check-videopage.html', context)