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
        if request.method == 'POST':
            short_thumbnail = request.FILES.get('short_thumbnail')
            short_title = request.POST.get('short_title')
            short_link = request.FILES.get('short_link')
            short_description = request.POST.get('short_description')

            obj = ShortsDetails(
                short_thumbnail = short_thumbnail,
                short_title = short_title,
                short_link = short_link,
                short_description = short_description,
                customer_name = request.user
            )
            obj.save()
            
            return redirect('profile')

        return render(request, 'shorts-upload.html')
    
    else:
        return redirect('login')
    
def editShort(request, id):
    if request.user.is_authenticated:
        short = ShortsDetails.objects.get(id=id)
        form = ShortsForm(request.POST or None, request.FILES or None, instance=short)
        check_user = short.customer_name.username 
        formImg = form.instance.short_thumbnail
        formLink = form.instance.short_link

        if request.user.username == check_user:
            if request.method == 'POST':

                if not request.FILES.get('short_thumbnail'):
                    form.instance.short_thumbnail = formImg
                
                if not request.FILES.get('short_link'):
                    form.instance.short_link = formLink

                print(request.FILES.get('short_thumbnail'), ' ', request.FILES.get('short_link'), ' ', request.POST.get('short_title'), ' ', request.POST.get('short_description'))
                
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