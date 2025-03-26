from django.shortcuts import render, redirect, HttpResponse
from .models import VideoDetails
from .forms import VideoForm
from django.contrib import messages
from shorts.models import ShortsDetails
from banner.models import BannerDetails
from django.db.models import Q
from datetime import datetime
from users.models import ProfileDetails
import random
from django.contrib.auth.models import User

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
    # print(lst1) # [(12, 2, 54), (12, 2, 54), (12, 2, 55), (12, 2, 56), (12, 4, 15)]

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

    lstOfUser = []
    for z1 in val1:
        lstOfUser += [z1['customer_name_id']]
    
    # print(lstOfUser)
    lstNameOfUser = []; lst__1 = []
    for z2 in lstOfUser:
        get_name = User.objects.get(id = z2)
        pf_get_data = ProfileDetails.objects.filter(NamesUser = get_name)
        lst__1 += [pf_get_data]
    
    for t1 in lst__1:
        for t2 in t1:
           lstNameOfUser += [t2.Channel_Name]
    DataCarringTwo = zip(val1, lstNameOfUser)


    random.shuffle(shorts)
    random.shuffle(ban2)

    while len(val1):
        if len(val1) == 8:
            break
        else:
            val1.pop()

    context = {
        'video': DataCarringTwo,
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
                
        profile = ProfileDetails.objects.get(NamesUser=video.customer_name)
        prof_img = profile.Profile_Image
        prof_data = profile.Channel_Name

        if other_videos:
            lst1 = []
            for i in other_videos:
                # geting query set
                f1 = ProfileDetails.objects.filter(NamesUser = i.customer_name)
                # excessing queryset with for loop
                for j in f1:
                    lst1 += [j.Channel_Name]

            other_datas_zip = zip(other_videos, lst1)
        
    except:
        return HttpResponse('page not found <strong> localhost:8000/video/{} </strong>'.format(video_data))
    
    context = {"video": video, "other_videos": other_datas_zip, 'prof_data' : prof_data, 'prof_img' : prof_img, 'other_data' : other_data}
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
                
        profile = list(video_profile); prof = []; count_prof = 1
        for i in profile:
            if (count_prof <= 3):
                if (i.Channel_Name != 'MediX User Profile') and (i.uName != 'yourmedix'):
                    prof += [i]
                    count_prof += 1
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

def videoUpload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            video_thumbnail = request.FILES.get('video_thumbnail')
            video_title = request.POST.get('video_title')
            video_link = request.FILES.get('video_link')
            video_description = request.POST.get('video_description')
            video_aim = request.POST.get('video_aim')
            customer_name = request.user

            video = VideoDetails(
                video_thumbnail=video_thumbnail,
                video_title=video_title,
                video_link=video_link,
                video_description=video_description,
                video_aim=video_aim,
                customer_name=customer_name,
            )
            video.save()

            messages.success(
                request, 'Your video has been uploaded successfully!'
            )
            return redirect('profile')

        return render(request, 'video-upload.html')

    else:
        return redirect('login')
def updateVideo(request, item_id):
    video = VideoDetails.objects.get(id=item_id)
    form = VideoForm(request.POST or None, request.FILES or None, instance=video)
    check_user = video.customer_name.username
    
    if request.user.is_authenticated:
        if request.user.username == check_user:
            if request.method == 'POST':
                print('print 1111')
                # print(form['video_thumbnail'], ' ', form['video_title'], ' ', form['video_description'], ' ', form['video_aim'], ' ', form['customer_name'])
                if form.is_valid():
                    video = form.save(commit=False)
                    video.customer_name = request.user
                    print('print 222')
                    video.save()
                    return redirect('profile')
                else:
                    print('not filled form')

            context = {'form': form, 'video': video}
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