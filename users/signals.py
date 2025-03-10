from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import ProfileDetails

@receiver(post_save, sender=User)
def build_private(sender, instance, created, **kwargs):
    if created:
        ProfileDetails.objects.create(NamesUser=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profiledetails.save()