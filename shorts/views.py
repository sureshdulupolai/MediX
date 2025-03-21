from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ShortsForm
from django.contrib import messages
from .models import ShortsDetails

# Create your views here.

def callVideo(request, st_id):
    short = get_object_or_404(ShortsDetails,id=st_id)
    context = {
        'short' : short,
    }
    return render(request, 'Open-Shorts.html', context)

@csrf_exempt
def shortUpload(request):
    if request.user.is_authenticated:
        form = ShortsForm()
        if request.method == 'POST':
            form = ShortsForm(request.POST,  request.FILES)
            if form.is_valid():
                messages.success( 
                    request, 'Your video uploaded successfully to system'
                )
                form.save()
                return redirect('shorts_upload')

        context = {'form': form}
        return render(request, 'shorts-upload.html', context)
    
    else:
        return redirect('login')
    
def editShort(request, id):
    short = ShortsDetails.objects.get(id=id)
    form = ShortsForm(request.POST or None, request.FILES or None, instance=short)
    check_user = short.customer_name.username 
    if request.user.is_authenticated:
       if request.user.username == check_user:
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect('profile')
                
            context = {
                'form' : form,
                'short': short,
                'check_user' : check_user,
            }
            return render(request, 'edit-short.html', context)
       
       else:
           return HttpResponse('Page Not Found')
    
    else:
        return redirect('page')