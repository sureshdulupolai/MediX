from django.db import models

# Create your models here.
class ProfileDetails(models.Model):
    Profile_Image = models.ImageField(upload_to='profile/')
    Name = models.CharField(max_length=100)
    Channel_Name = models.CharField(max_length=100)
    Title = models.CharField(max_length=100)

    def __str__(self):
        return self.Name