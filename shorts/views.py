from django.shortcuts import render, redirect, get_object_or_404
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