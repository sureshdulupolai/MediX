from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class ShortsDetails(models.Model):
    short_thumbnail = models.ImageField(upload_to='thum/')
    short_title = models.CharField(max_length=1000)
    short_link = models.FileField(upload_to='video/')
    short_description = models.TextField(max_length=1000, null=True, blank=True)
    created_date = models.DateField(default=timezone.now)
    customer_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    view = models.FloatField(default=230.64)

    def __str__(self):
        return self.short_title