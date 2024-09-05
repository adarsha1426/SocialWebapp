from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings

@receiver(post_save,sender=False)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile is created.")

@receiver(post_save,sender=False)
def save_profile(sender,instance,**kwargs):
    instance.save()                                    
post_save.connect(create_profile,sender=settings.AUTH_USER_MODEL)