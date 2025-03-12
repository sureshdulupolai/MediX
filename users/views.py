from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from videos.models import VideoDetails
from .models import ProfileDetails
from banner.models import BannerDetails

# Create your views here.
def SignupPage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                'hello {}, yo have been successfully signup up'.format(username)
            )
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()
        messages.success(
            request,
            'Your \'Register\' is Successfully, then you will redirect to login page',
        )

    context = {
        'form' : form,
    }
    return render(request, 'signup.html', context)

def Login_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)  # django built-in login form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')     
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)

def Logout_in(request):
    logout(request)
    return redirect('home')

def logout_ask(request):
    return render(request, 'logout.html')

def ProfilePage(request):
    if request.user.is_authenticated:
        # data = VideoDetails.objects.get(id=8)
        data1 = VideoDetails.objects.filter(customer_name=request.user.id)
        profile = ProfileDetails.objects.filter(NamesUser=request.user).first() 
        Banner = BannerDetails.objects.filter(uName=request.user.id)

        context = {
            # 'form' : data,
            'form1' : data1,
            'profile' : profile,
            'banner' : Banner,
        }
        # print(profile.Profile_Image)
        return render(request, 'profile.html', context)

    else:
        return redirect ('login')

def ProfileEdit(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            messages.success(request,'You Can Edit Your Profile Here')

        user_profile = ProfileDetails.objects.get(NamesUser=request.user)
        form = ProfileForm(request.POST or None, request.FILES or None, instance=user_profile)  # Pre-fill form with existing data
        v1 = form.instance.uName
        
        if request.method == 'POST':
            print(form.instance.Profile_Image)
            if form.is_valid():
                print(form.instance.Profile_Image)
                if form.instance.uName == v1:
                    print(form.instance.Profile_Image)
                    form.save()
                    print(form.instance.Profile_Image)
                    return redirect('profile')
                else:
                    lst1 = []; c1 = 0; user_details = ProfileDetails.objects.all().values(); value1 = form.instance.uName
                    for i in user_details:
                        lst1 += [i['uName']]
                    for j in lst1:
                        if value1 == j: c1 = 1
                        else: continue
                    if c1 == 0:
                        form.save()
                        return redirect('profile')
                    else: messages.warning(request,'Nickname Already Exist "{}", Choose another Nickname'.format(value1))
                
        context = {'form': form}
        return render(request, 'editProfile.html', context)

    return redirect('login')

