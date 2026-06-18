from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import os



#user Directory

def user_directory(instance, filename):
    return f'profile_pic/user_{instance.user.username}/{filename}'
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defualt.jpg', upload_to=user_directory)
    bio = models.TextField(blank=True, max_length=500)

    def __str__(self):
        return f'{self.user.username}Proifle'
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()