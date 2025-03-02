from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import bannerForm


# Create your views here.
def bannerPage(request):
    form = bannerForm()
    if request.method == "GET":
        messages.info(request, "The price to upload a banner is $2")
    if request.method == 'POST':
        form = bannerForm(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'bannerUpload.html', context)