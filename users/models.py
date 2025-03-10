from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ProfileDetails(models.Model):
    Profile_Image = models.ImageField(default='profile/user_profile.jpg', upload_to='profile/', max_length=2000)
    NamesUser = models.OneToOneField(User, on_delete=models.CASCADE, default='Your Profile')
    Channel_Name = models.CharField(max_length=100, default='MediX User Profile')
    uName = models.CharField(max_length=100, default='yourmedix')

    def __str__(self):
        return self.Channel_Name