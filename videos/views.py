from django.shortcuts import render, redirect, HttpResponse
from .models import VideoDetails
from .forms import VideoForm
from django.contrib import messages
from shorts.models import ShortsDetails
from banner.models import BannerDetails, BannerUploadUnSuccess, BannerTimeOver
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils.timezone import make_naive
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
    # Video Title Len Checking
    for i in val:
        title = i['video_title']
        if len(title) >= 32:
            val1 += [i]
            a1 += 1
        else:
            continue
    
    # Collecting Time Of Enter Data in Model
    lst1 = []
    for i in ban:
        date_part = int(i['banner_datetime'].strftime("%d")); time_part = i['banner_datetime'].strftime("%H:%M")
        t1 = int(time_part[0:2]); t2 = int(time_part[3:])
        lst1 += [(date_part, t1, t2)]
    # print(lst1) # [(12, 2, 54), (12, 2, 54), (12, 2, 55), (12, 2, 56), (12, 4, 15)]

    # Finding Current Day Timing
    now = datetime.now(); date1 = int(now.strftime("%d")); time_now = now.strftime("%H:%M")
    t3 = int(time_now[0:2]); t4 = int(time_now[3:])
    current_day_time = (date1, t3, t4)
    
    # print(current_day_time) - (18, 11, 11)
    # date - hr - minute
    # print(current_day_time, " ", lst1) - (18, 11, 14)   [(12, 2, 54), (12, 2, 54), (12, 2, 55), (12, 2, 56), (12, 4, 15)]

    # Banner Checking
    ban1 = []; ban2 =[]
    for i in range(len(lst1)):
        currentYear = now.year; AtLeast = 10; setMonths = 5

        # currentYear , month, day, hour, minute
        dates = lst1[i][0]; hours = lst1[i][1]; minutes = lst1[i][2]
        banner_time = datetime(currentYear, setMonths, dates, hours, minutes)

        # Get the current date and time
        now = datetime.now(); month = now.month; day = now.day; hour = now.hour; minute = now.minute
        current_datetime = datetime(currentYear, month, day, hour, minute)
        cutoff = current_datetime - timedelta(days=AtLeast)

        # if (lst1[i][ad] == current_day_time[ad]) or (lst1[i][ad] >= (current_day_time[ad] - check_value)):
        if banner_time >= cutoff:
            ban1 += [lst1[i]]; ban2 += [ban[i]]

    random.shuffle(val1)

    # Collecting All User Name To Display Name Home Page Video and Shorts
    lstOfUser = []
    for z1 in val1:
        print(z1['customer_name_id'])
        lstOfUser += [z1['customer_name_id']]
    
    # filtering all the records that comes in lstofuser
    # print(lstOfUser)
    lstNameOfUser = []; lst__1 = []
    for z2 in lstOfUser:
        get_name = User.objects.get(id = z2)
        pf_get_data = ProfileDetails.objects.filter(NamesUser = get_name)
        lst__1 += [pf_get_data]
    
    # Collecting Name of User That Video Showing in Display
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
                if (i.Channel_Name != 'MediX User Profile') and (i.uName != 'yourmedix') and (i.Profile_Image != 'profile/user_profile.jpg'):
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
    if request.user.is_authenticated:
        video = VideoDetails.objects.get(id=item_id)
        form = VideoForm(request.POST or None, request.FILES or None, instance=video)
        check_user = video.customer_name.username
        formImg = form.instance.video_thumbnail
        formLink = form.instance.video_link

        if request.user.username == check_user:
            if request.method == 'POST':
                # Check if the file fields are empty, retain old files if not updated
                if not request.FILES.get('video_thumbnail'):
                    form.instance.video_thumbnail = formImg
                
                if not request.FILES.get('video_link'):
                    form.instance.video_link = formLink

                print(request.FILES.get('video_thumbnail'), ' ', request.FILES.get('video_link'), ' ', request.POST.get('video_title'), ' ', request.POST.get('video_description'))

                if form.is_valid():
                    form.save()
                    return redirect('profile')
                
            context = {
                'form': form,
                'video': video,
                'check_user': check_user,
            }
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
            # print("in shorts", 1)
            a2.delete()
            return redirect('profile')
        else:
            a1 = VideoDetails.objects.get(video_title=video_title)
            # print("In video", 2)
            a1.delete()
            return redirect('profile')
    else:
        return HttpResponse('Page Not Found, check link properly')
    
# --------------------------------------------------------------------------------------
# Only Suresh Can Check This Link
def PustBannerData(request, UserData):
    if request.user.is_authenticated:
        if request.user.username == 'suresh':
            if UserData == 'transfer':
                BD = BannerDetails.objects.all().values()
                for BD1 in BD:
                    UserName = User.objects.get(id = BD1['uName_id'])
                    DateAndTime = str(BD1['banner_datetime']); Date = DateAndTime[5:10]; Hours = DateAndTime[11:19]
                    BUS = BannerTimeOver(
                        BTO_Title = BD1['banner_title'],
                        BTO_Image = BD1['banner_img'],
                        BTO_Contact = BD1['contact_no'],
                        BTO_Username = str(UserName.username),
                        BTO_Issue_Date = Date,
                        BTO_Hr_Min_Sec = Hours,
                    )
                    BUS.save()
                return HttpResponse('Done')

            elif UserData == 'deletedata':
                BDData = BannerDetails.objects.all()
                BUUSData = BannerTimeOver.objects.all().values()

                for BUUS1 in BUUSData:
                    for BD2 in BDData:
                        UName = User.objects.get(id=BD2.uName_id)
                        if (BUUS1['BTO_Username'] == str(UName.username) and BUUS1['BTO_Title'] == BD2.banner_title and BUUS1['BTO_Contact'] == BD2.contact_no):
                            BD2.delete()

                return HttpResponse('Check')
            
            elif UserData == 'checkdata':
                return HttpResponse('Done 3!')
            
            elif UserData == 'permonthupdate':
                setDateAtEnd = 10; count = 0
                banners = BannerDetails.objects.all()
                if len(banners) > 0:
                    for BDS in banners:
                        banner_time = make_naive(BDS.banner_datetime)  # from loop
                        ten_days_later = banner_time + timedelta(days=setDateAtEnd)

                        # Compare with fixed time that comes from loop
                        if datetime.now() >= ten_days_later:
                            user = User.objects.get(id=BDS.uName_id)
                            date = str(banner_time)[5:10]
                            time_str = str(banner_time)[11:19]

                            BUS = BannerTimeOver(
                                BTO_Title=BDS.banner_title,
                                BTO_Image=BDS.banner_img,
                                BTO_Contact=BDS.contact_no,
                                BTO_Username=str(user.username),
                                BTO_Issue_Date=date,
                                BTO_Hr_Min_Sec=time_str,
                            )
                            BUS.save()
                            BDS.delete()
                            count += 1

                    return HttpResponse('This is The Data Of BannerDetails List Added Into BannerTimeOver Model : {}'.format(count))
                
                else:
                    return HttpResponse('This is The Len Of BannerDetails List : {}'.format(len(banners)))
            
            else:
                return render(request, 'page_not_found.html')
            
        else:
            return render(request, 'page_not_found.html')
    else:
        return render(request, 'page_not_found.html')