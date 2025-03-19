from django.shortcuts import render, redirect, HttpResponse
from .models import VideoDetails
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

# def pageNotFound(request, data_link):
#     return render(request, 'page_not_found.html')

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
    # print(lst1) - [(12, 2, 54), (12, 2, 54), (12, 2, 55), (12, 2, 56), (12, 4, 15)]

    now = datetime.now(); date1 = int(now.strftime("%d")); time_now = now.strftime("%H:%M")
    t3 = int(time_now[0:2]); t4 = int(time_now[3:])
    current_day_time = (date1, t3, t4)
    
    # print(current_day_time) - (18, 11, 11)
    # date - hr - minute
    # print(current_day_time, " ", lst1) - (18, 11, 14)   [(12, 2, 54), (12, 2, 54), (12, 2, 55), (12, 2, 56), (12, 4, 15)]

    ban1 = []; ban2 =[]; check_value = 10; ad = 0
    for i in range(len(lst1)):
        if (lst1[i][ad] == current_day_time[ad]) or (lst1[i][ad] >= (current_day_time[ad] - check_value)):
            ban1 += [lst1[i]]; ban2 += [ban[i]]
        
    # print(len(ban))
    # print(len(ban2))
    random.shuffle(val1)
    random.shuffle(shorts)
    random.shuffle(ban2)

    while len(val1):
        if len(val1) == 8:
            break
        else:
            val1.pop()

    context = {
        'video': val1,
        'shorts': shorts,
        'banner': ban2,
    }
    return render(request, 'homepage.html', context)


def openVideoPage(request, video_data=None):
    video = None
    other_videos = VideoDetails.objects.all()
    other_data = []

    try:
        if video_data:
            videos = VideoDetails.objects.get(id=video_data)
            video = VideoDetails.objects.filter(video_title=videos).first()

            if video:
                other_videos = list(other_videos.exclude(id=video.id))
                random.shuffle(other_videos)
            
            for vid in other_videos:
                try:
                    other_profile = ProfileDetails.objects.get(NamesUser=vid.customer_name)
                    other_data.append({'prof_data': other_profile.Channel_Name, 'prof_img': other_profile.Profile_Image,})
                except ProfileDetails.DoesNotExist:
                    pass

        # print(other_data)
                
        profile = ProfileDetails.objects.get(NamesUser=video.customer_name)
        prof_img = profile.Profile_Image
        prof_data = profile.Channel_Name

    except:
        return HttpResponse('page not found <strong> localhost:8000/video/{} </strong>'.format(video_data))
    
    context = {"video": video, "other_videos": other_videos, 'prof_data' : prof_data, 'prof_img' : prof_img, 'other_data' : other_data}
    return render(request, 'Open-Video.html', context)

def searchPage(request):
    try:
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
        # print(profile)
        prof = []; count_prof = 1
        for i in profile:
            if (count_prof <= 3):
                if (i.Channel_Name != 'MediX User Profile') and (i.uName != 'yourmedix'):
                    prof += [i]
                    count_prof += 1
                    # print(count_prof)
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
    except:
        return render(request, 'page_not_found.html')

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

def videoDelete(request, video_title):
    if request.user.is_authenticated:
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
    else:
        return HttpResponse('What you want to delete ?, when you are not login')

def successfullydeleted(request, video_title):
    if request.user.is_authenticated:
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
    else:
        return HttpResponse('Page Not Found, check link properly')
