from django.db import models
from django.utils import timezone

# Create your models here.
class ShortsDetails(models.Model):
    short_thumbnail = models.ImageField(upload_to='thum/')
    short_title = models.CharField(max_length=100)
    short_link = models.FileField(upload_to='video/')
    short_description = models.CharField(max_length=200)
    created_date = models.DateField(default=timezone.now)
    customer_name = models.CharField(max_length=100)
    view = models.FloatField(default=230.64)

    def __str__(self):
        return self.short_title