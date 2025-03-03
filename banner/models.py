from django.db import models
from django.utils import timezone

# Create your models here.
class BannerDetails(models.Model):
    banner_img = models.ImageField(upload_to='banner/')
    banner_title = models.CharField(max_length=200)
    banner_datetime = models.DateTimeField(default=timezone.now)
    contact_no = models.CharField(max_length=10)

    def __str__(self):
        return self.banner_title