from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class BannerDetails(models.Model):
    banner_img = models.ImageField(upload_to='banner/')
    banner_title = models.CharField(max_length=200)
    banner_datetime = models.DateTimeField(default=timezone.now)
    contact_no = models.CharField(max_length=10)
    uName = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    # add column for month

    def __str__(self):
        return self.banner_title
    
class BannerUploadUnSuccess(models.Model):
    banner_Images = models.ImageField(upload_to='BannerTime/')
    banner_t = models.CharField(max_length=200)
    banner_date = models.DateTimeField(default=timezone.now)
    contact_no = models.CharField(max_length=15)
    UserName = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    # add column for month after shift all data into BannerTimeOver model

    def __str__(self):
        return str(
            (self.banner_t, self.UserName.username)
        )
    
class BannerTimeOver(models.Model):
    BTO_Title = models.CharField(max_length=200)
    BTO_Image = models.ImageField(upload_to='BannerOver/')
    BTO_Contact = models.CharField(max_length=15)
    BTO_Username = models.CharField(max_length=100)
    BTO_Issue_Date = models.CharField(max_length=100)
    BTO_End_Date = models.DateTimeField(default=timezone.now)
    BTO_Month = models.IntegerField(default=datetime.now().month)
    BTO_Hr_Min_Sec = models.CharField(max_length=20, default='None')

    def __str__(self):
        return str(
            (self.BTO_Title, ' ', self.BTO_Username)
        )

# class YourModel(models.Model):
#     # Other fields
#     current_month = models.IntegerField()

#     def save(self, *args, **kwargs):
#         self.current_month = datetime.now().month
#         super().save(*args, **kwargs)
