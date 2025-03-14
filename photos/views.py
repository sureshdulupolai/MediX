from django.shortcuts import render, redirect
# from .forms import PostWithImagesForm
# from .models import PostImage

# Create your views here.
def uploadPhoto(request):
    # if request.method == "POST":
    #     form = PostWithImagesForm(request.POST, request.FILES)
    #     images = request.FILES.getlist('images')  

    #     if form.is_valid():
    #         post = form.save()
    #         for image in images:
    #             PostImage.objects.create(post=post, image=image)  
    #         return redirect('upload_post')
    #     form = PostWithImagesForm()

    # context = {'form': form}
    # context
    return render(request, 'photos-upload.html', )