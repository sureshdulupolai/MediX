from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from videos.models import VideoDetails
from .models import ProfileDetails

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
        context = {
            # 'form' : data,
            'form1' : data1,
            'profile' : profile,
        }
        # print(profile.Profile_Image)
        return render(request, 'profile.html', context)

    else:
        return redirect ('login')

def ProfileEdit(request):
    if request.user.is_authenticated:
        try:
            user_profile = ProfileDetails.objects.get(NamesUser=request.user)
        except ProfileDetails.DoesNotExist:
            user_profile = ProfileDetails(NamesUser=request.user)

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = ProfileForm(instance=user_profile)  # Pre-fill form with existing data

        context = {'form': form}
        return render(request, 'editProfile.html', context)

    return redirect('login')