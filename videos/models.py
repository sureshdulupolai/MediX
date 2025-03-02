from django.db import models
from django.utils import timezone


# Create your models here.
class VideoDetails(models.Model):
    video_thumbnail = models.ImageField(upload_to='thum/')
    video_title = models.CharField(max_length=200)
    video_link = models.FileField(upload_to='video/')
    video_description = models.CharField(max_length=5000)
    created_date = models.DateField(default=timezone.now)
    video_aim = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    view = models.FloatField(default=120.20)

    def __str__(self):
        return self.video_title
    
class VideoCategory(models.Model):
    options = [
        ('comedy', 'comedy'),
        ('song', 'song'),
        ('movie', 'movie'),
        ('study', 'study'),
        ('games', 'games'),
        ('other activity', 'other activity'),
    ]

    vd_category = models.CharField(max_length=50, choices=options)
    vd_primary_key = models.ForeignKey(VideoDetails, related_name='video_primary', on_delete=models.CASCADE)

    def __str__(self):
        return str((self.vd_category, self.vd_primary_key.video_title))


# ---------------------------------------------------------------------------------------------------------------
# CASCADE:
# VideoDetails (Parent Table)
# VideoCategory (Child Table)
# ForeignKey: vd_primary_key ka connection VideoDetails se hai.
# on_delete=models.CASCADE ka Matlab
# Agar VideoDetails ka koi ek record delete hota hai, toh usse linked VideoCategory ka record bhi automatically delete ho jayega.


# models.CASCADE - Parent delete → Child delete 
# models.SET_NULL - Parent delete → Child ka FK NULL ho jaye (null=True hona chahiye)
# models.SET_DEFAULT - Parent delete → Child ka FK default value le le
# models.PROTECT - Parent delete hone nahi dega jab tak child exist kare 
# models.DO_NOTHING - Kuch nahi karega, but error aa sakta hai agar child orphan ho gaya 