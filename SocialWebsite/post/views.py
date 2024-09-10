from django.shortcuts import render
from userdetail.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post,Comment
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,HttpResponse
from django.db.models import Count

from django.contrib import messages
# Create your views here.
@login_required(login_url='userdetail:login')
def home(request):
    current_user = request.user

    try:
        user_profile=Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
        user_profile,created = Profile.objects.get_or_create(user=request.user)

    # Exclude posts created by the current user's profile
    post = Post.objects.exclude(user=user_profile)
    
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Fetching full model instances instead of values()
    profile_objects = Profile.objects.exclude(user=current_user)
    print(current_user)
    context = {
        'posts': post,
        'profile': profile,
        'profile_objects': profile_objects,
    }
    return render(request, "post/homepage.html", context)

def base(request):
    user = get_object_or_404(User, username=request.user)
    profile=Profile.objects.get(user=request.user)
    print(profile.profile_pic) 
    return render(request,"base.html",{'profile':profile})

@login_required
def create_post(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)  # Get the Profile of the logged-in user
        if request.method == 'POST':
            post_form = PostForm(request.POST ,request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)  # Don't save to the database yet
                post.user = profile  # Assign the Profile, not the User
                post.save()  # Now save the post
                messages.success(request, "Post created successfully!")
                return redirect('post:home')  # Redirect after successful post creation
            else:
                messages.error(request, "Error while posting form")
        else:
            post_form = PostForm()

    else:
        return redirect('post:home')  
    return render(request, 'post/create_post.html', {'post_form': post_form})

def postdetail(request,post_slug):
    post=get_object_or_404(Post,slug=post_slug)
    comments = Comment.objects.filter(post=post)
    comment_co=Comment.objects.annotate(Count('body')).filter(post=post)
    comment_count=len(comment_co)
    print(comment.get_username() for comment in comments)
    return render(request,'post/post.html',{'post':post,'comments':comments,'comment_count':comment_count})

def like(request,post_slug):
    post=get_object_or_404(Post,slug=post_slug)
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
    else:
        post.likes.add(request.user.profile)

    return redirect('post:home')

@login_required
def create_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user.profile # Assuming comments are linked to a user
            comment.save()
            return redirect('post:home')  # Redirect after successful comment
    else:
        form = CommentForm()
    return render(request, 'post/create_comment.html', {'comment_form': form, 'post': post})

def share():
    pass