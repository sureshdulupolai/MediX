from django.shortcuts import render, redirect
from .forms import PostWithImagesForm
from .models import PostImage

# Create your views here.
def uploadPhoto(request):
    if request.method == "POST":
        form = PostWithImagesForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')  # ✅ Get multiple images

        if form.is_valid():
            post = form.save()  # ✅ Save post first
            for image in images:
                PostImage.objects.create(post=post, image=image)  # ✅ Save each image
            return redirect('upload_post')  # ✅ Redirect to post list page
    else:
        form = PostWithImagesForm()

    context = {'form': form}
    return render(request, 'photos-upload.html', context)