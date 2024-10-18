from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    bio=models.CharField(max_length=100,blank=True,null=True)
    date_of_birth=models.DateField(blank=True,null=True)
    profile_pic=models.ImageField(blank=True,upload_to="static/profile_images")
    following = models.ManyToManyField(
    "self", 
    related_name="followed_by", 
    symmetrical=False, 
    blank=True
)#This indicates a relationship between instances of the same model (i.e., a user can follow other users from the same model).
    
    def __str__(self) :
        return f"{self.user.first_name}"
    
    def follow(self, profile):
        if not self.is_following(profile):
            self.following.add(profile)

    def unfollow(self, profile):
        if self.is_following(profile):
            self.following.remove(profile)
    
    def count_following(self):
        return self.following.count()

    def count_followed_by(self):
        return self.followed_by.count()




    def get_absolute_url(self):
        return reverse("userdetail:user_profile", kwargs={"username": self.user.username})

    
    def is_following(self, profile):
        return self.following.filter(pk=profile.pk).exists()