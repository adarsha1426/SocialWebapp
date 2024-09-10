from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True,null=True)
    profile_pic=models.ImageField(blank=True,upload_to="static/profile_images")
    follow = models.ManyToManyField(
    "self", 
    related_name="followed_by", 
    symmetrical=False, 
    blank=True
)#This indicates a relationship between instances of the same model (i.e., a user can follow other users from the same model).
    def __str__(self) :
        return f"{self.user.first_name}"