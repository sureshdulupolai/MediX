from django.shortcuts import render, redirect, HttpResponse
from .models import VideoDetails, VideoCategory
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import VideoForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from shorts.models import ShortsDetails
from banner.models import BannerDetails
from django.db.models import Q
from datetime import datetime, date
from django.contrib.auth.models import User
from users.models import ProfileDetails
import random

def short():
    short = ShortsDetails.objects.all().values()
    return short

def callVideo():
    return VideoDetails.objects.all().values()

def homepage(request):
    ban = list(BannerDetails.objects.all().values())
    val = callVideo()
    
    shorts = list(short())
    val1 = []; a1 = 0
    for i in val:
        title = i['video_title']
        if len(title) >= 32:
            val1 += [i]
            a1 += 1
        else:
            continue
    
    lst1 = []
    for i in ban:
        date_part = int(i['banner_datetime'].strftime("%d")); time_part = i['banner_datetime'].strftime("%H:%M")
        t1 = int(time_part[0:2]); t2 = int(time_part[3:])
        lst1 += [(date_part, t1, t2)]
    # print(lst1)

    now = datetime.now(); date1 = int(now.strftime("%d")); time_now = now.strftime("%H:%M")
    t3 = int(time_now[0:2]); t4 = int(time_now[3:])
    current_day_time = (date1, t3, t4)
    date2 = date1 - 1
    # print(current_day_time)

    # if str(date2) in lst1:
    #     print('hi')
    # else:
    #     print('hello')

    random.shuffle(val1)
    random.shuffle(shorts)
    random.shuffle(ban)

    while len(val1):
        if len(val1) == 8:
            break
        else:
            val1.pop()

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
        if video_data.isdigit():  
            video = VideoDetails.objects.filter(id=video_data).first()
        else:
            video = VideoDetails.objects.filter(video_title__icontains=video_data) | \
                    VideoDetails.objects.filter(video_description__icontains=video_data)
            
            video_profile = ProfileDetails.objects.filter(
                    Q(uName__icontains=video_data)  | \
                    Q(Channel_Name__icontains=video_data)
            )

            short = ShortsDetails.objects.filter(short_title__icontains=video_data) | \
                    ShortsDetails.objects.filter(short_description__icontains=video_data)
            
    profile = list(video_profile)
    print(profile)
    prof = []; count_prof = 1
    for i in profile:
        if (count_prof <= 3):
            if (i.Channel_Name != 'MediX User Profile') and (i.uName != 'yourmedix'):
                prof += [i]
                count_prof += 1
                print(count_prof)
        else:
            break

    val = list(video)
    shorts = list(short)
    if len(val) >= 4:
        while len(val):
            if len(val) % 4 == 0:
                break
            else:
                val.pop()
    
    random.shuffle(val)
    random.shuffle(shorts)

    context = {
        'video': val,
        'data' : data,
        'video_profile' : prof,
        'shorts' : shorts,
    }
    return render(request, 'searchPage.html', context)

# @csrf_exempt
def videoUpload(request):
    if request.user.is_authenticated:
        form = VideoForm()
        if request.method == 'POST':
            form = VideoForm(request.POST,  request.FILES)
            if form.is_valid():
                # form.instance.admin = request.user.username
                messages.success( 
                    request, 'Your video uploaded successfully to system'
                )
                form.save()
                return redirect('video_upload')

        context = {'form': form}
        return render(request, 'video-upload.html', context)

    else:
        return redirect ('login')
    
def updateVideo(request, item_id):
    video = VideoDetails.objects.get(id=item_id)
    form = VideoForm(request.POST or None, request.FILES or None, instance=video)
    check_user = video.customer_name.username

    if request.user.is_authenticated:
       if request.user.username == check_user:
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect('profile')
            context = {'form' : form,'video': video,}
            return render(request, 'edit-video.html', context)
       else:
           return HttpResponse('Page Not Found')
    else:
        return redirect('login')
           
 
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

def videoDelete(request, video_title):
    a1 = None
    a2 = None

    try:
        if video_title.isdigit():
            item = int(video_title)
            a2 = ShortsDetails.objects.get(id=item)
            video_title = a2.short_title
        else:
            a1 = VideoDetails.objects.get(video_title=video_title)
    except (VideoDetails.DoesNotExist, ShortsDetails.DoesNotExist):
        pass

    context = {
        'a1' : a1,
        'a2' : a2,
        'video_name' : video_title,
    }
    return render(request, 'video-delete.html', context)

def successfullydeleted(request, video_title):
    a1 = None
    a2 = None

    if video_title.isdigit():
        item = int(video_title)
        a2 = ShortsDetails.objects.get(id=item)
        print("in shorts", 1)
        a2.delete()
        return redirect('profile')
    else:
        a1 = VideoDetails.objects.get(video_title=video_title)
        print("In video", 2)
        a1.delete()
        return redirect('profile')


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