from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import bannerForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def bannerPage(request):
    form = bannerForm()
    if request.method == 'POST':
        form = bannerForm(request.POST,  request.FILES)
        if form.is_valid():
            messages.success( 
                request, 'You need to pay for this banner upload'
            )
            form.save()
            return redirect('banner')

    context = {'form': form}
    return render(request, 'bannerUpload.html', context)