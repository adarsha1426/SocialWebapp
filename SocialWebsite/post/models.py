from django.db import models
from userdetail.models import Profile
from django.conf import settings
from django.utils.text import slugify
import uuid
class Post(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    body=models.CharField(max_length=280,blank=True)
    image=models.ImageField(blank=True,upload_to='static/post_images')
    created=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(Profile,related_name="post_like",blank=True)

    def generate_slug(self):
        if self.body:
            slug = slugify(str(self.body[:10]) +"-" +str(self.id)+str(self.user))
        else:
            slug = slugify(f"post-{uuid.uuid4().hex[:8]}")
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super(Post,self).save(*args,**kwargs)
   

    def count_like(self):
        return self.likes.count()
    def get_username(self):
        return self.user

    def __str__(self):
        return f"{self.user} post created on  {self.created} ."

class Comment(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,max_length='300',on_delete=models.CASCADE)
    body=models.CharField(max_length=200,blank=True)
   
    likes=models.ManyToManyField(Profile,related_name="comment_like",blank=True)
    
    def count_like(self):
        return self.likes.count()
    
    def get_username(self):
        return f"{self.user}"

    

    def __str__(self):
        return f"{self.body}"
    

