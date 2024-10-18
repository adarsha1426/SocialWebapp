from django.shortcuts import render
from userdetail.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post,Comment
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse

from django.db.models import Count

from django.conf import settings
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
    posts = Post.objects.exclude(user=user_profile)
    
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile, created = Profile.objects.get_or_create(user=request.user)
    
    
    # Fetching full model instances instead of values()
    profile_objects = Profile.objects.exclude(user=current_user)
    user_profile = User.objects.exclude(id=current_user.id).values() 
    context = {
        'posts': posts,
        'profile': profile,
        'profile_objects': profile_objects,
        'user_profile': user_profile,
        
    }
    return render(request, "post/homepage.html", context)

#nav bar
def base(request):
    user = get_object_or_404(User, username=request.user)
    profile=Profile.objects.get(user=request.user)
    print(profile.profile_pic) 
    return render(request,"base.html",{'profile':profile})

#creating post
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

#post detail
def postdetail(request,post_slug):
    post=get_object_or_404(Post,slug=post_slug)
    comments = Comment.objects.filter(post=post)
    comment_co=Comment.objects.annotate(Count('body')).filter(post=post)
    comment_count=len(comment_co)
    print(comment.get_username() for comment in comments)
    return render(request,'post/post.html',{'post':post,'comments':comments,'comment_count':comment_count})

#post like
def like(request,post_slug):
    post=get_object_or_404(Post,slug=post_slug)
    msg=False
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
        msg=False
       
    else:
        post.likes.add(request.user.profile)
        msg=True
        
    like_count=post.count_like()
    return JsonResponse({
        'msg': msg,
        'like_count': like_count,
    })

#Creating comment
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



def your_post(request, id):
    user = request.user
    profile = get_object_or_404(Profile, user=user)  # Get the profile based on the user

    # Now filter posts using the profile (not the user)
    posts = Post.objects.filter(user=profile)  # Filter by profile since `user` is a ForeignKey to `Profile`

    return render(request, "post/your_post.html", {'posts': posts})

@login_required
def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    print(post.user)
    print(f"reuested user: {request.user}")
    if post.user.user==request.user:
        post.delete()
        return redirect('post:home')
    else:
        return HttpResponse(request,"Error")
    
def delete(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if post.user.user == request.user:
        return render(request, "post/delete_post.html", {'post': post})
    else:
        return HttpResponse(f"{request.user} Post user {post.user.user}You are not authorized to delete this post.")
