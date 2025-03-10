from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ProfileDetails(models.Model):
    Profile_Image = models.ImageField(upload_to='profile/')
    NamesUser = models.OneToOneField(User, on_delete=models.CASCADE)
    Channel_Name = models.CharField(max_length=100)
    uName = models.CharField(max_length=100)

    def __str__(self):
        return self.Channel_Name