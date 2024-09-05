from django.db import models
from userdetail.models import Profile
from django.conf import settings
from django.utils.text import slugify

class Post(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)
    body=models.CharField(max_length=280,blank=True)
    image=models.ImageField(blank=True,upload_to='static/post_images')
    like_count=models.IntegerField(default=0,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(Profile,related_name="post_like",blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Post,self).save(*args,**kwargs)


    def __str__(self):
        return f"{self.user} post created on  {self.created} ."

class Comment(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,max_length='300',on_delete=models.CASCADE)
    body=models.CharField(max_length=200,blank=True)
    like_count=models.IntegerField(default=0,blank=True)
    likes=models.ManyToManyField(Profile,related_name="comment_like",blank=True)
    

    def __str__(self):
        return f"{self.user.first_name} has commented  on  {self.post.title}"
    