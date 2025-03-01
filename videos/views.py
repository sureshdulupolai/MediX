from django.shortcuts import render, redirect
from .models import VideoDetails, VideoCategory
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import VideoForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from shorts.models import ShortsDetails
import random

def short():
    short = ShortsDetails.objects.all().values()
    return short

# Create your views here.
def callVideo():
    video = VideoDetails.objects.all().values()
    return video

def homepage(request):
    val = callVideo()
    shorts = list(short())
    val1 = []; val2 = []
    for i in val:
        if len(i['video_title']) <= 32:
            if i['customer_name']:
                i['customer_name'] = i['customer_name'].title()
            val1 += [i]
        else:
            if i['customer_name']:
                i['customer_name'] = i['customer_name'].title()
            val2 += [i]
    for j in shorts:
        if j['customer_name']:
                j['customer_name'] = j['customer_name'].title()

    random.shuffle(val1)
    random.shuffle(val2)
    random.shuffle(shorts)

    context = {
        'video' : val1,
        'video2' : val2,
        'shorts' : shorts,
    }
    return render(request, 'homepage.html', context)


def openVideoPage(request, video_data=None):
    video = None
    other_videos = VideoDetails.objects.all()

    if video_data:
        if video_data.isdigit():
            video = VideoDetails.objects.filter(id=video_data).first()
        else: 
            video = VideoDetails.objects.filter(video_title__icontains=video_data) | \
                    VideoDetails.objects.filter(customer_name__icontains=video_data) | \
                    VideoDetails.objects.filter(video_description__icontains=video_data)
            video = video.first()

    elif request.method == 'POST' and 'videoName' in request.POST:
        video_data = request.POST['videoName']
        if video_data.isdigit():  
            video = VideoDetails.objects.filter(id=video_data).first()
        else:
            video = VideoDetails.objects.filter(video_title__icontains=video_data) | \
                    VideoDetails.objects.filter(customer_name__icontains=video_data) | \
                    VideoDetails.objects.filter(video_description__icontains=video_data)
            video = video.first()

    if video:
        # removing a particular video, which is running on
        other_videos = other_videos.exclude(id=video.id)


    context = {"video": video, "other_videos": other_videos}  
    return render(request, 'Open-Video.html', context)

@csrf_exempt
def videoUpload(request):
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