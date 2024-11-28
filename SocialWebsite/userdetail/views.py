from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import LoginForm,RegisterForm,ProfileEditForm,UpdateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Profile
from post.models import Post,Comment
from post.views import postdetail
from django.urls import reverse
# Create your views here.

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate user with form data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)  # Only call login if user is valid
                return redirect("post:home")
            elif user is not None and not user.is_active:
                messages.error(request, "Account is inactive.")
            else:
            
                messages.error(request, "Invalid login credentials.")
                return render(request, "userdetail/login.html", {'form': form})
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, "userdetail/login.html", {'form': form})
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)  # This will log out the user
        messages.success(request, "You have been logged out.")  # Add a success message
    
    # Redirect to home or login page after logging out
    return render(request,'userdetail/logout.html')
    
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please use another email.")
            else:
                user.set_password(password)
                user.save()

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Registration successful!")
                    return redirect('post:home')
                else:
                    messages.error(request, "User authentication failed.")

    return render(request, 'userdetail/register.html', {"form": form})
    
@login_required(login_url='userdetail:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Keeps the user logged in.
            messages.success(request, 'Your password was successfully updated!')
            return render(request,'userdetail/password_change_done.html')
        else:
            messages.error(request,'Invalid .')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userdetail/password_change.html', {'form': form})
@login_required(login_url='userdetail:login')
def profile(request):
  
    profile=Profile.objects.get(user=request.user)
    current_user = request.user

    try:
        user_profile=Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
        user_profile,created = Profile.objects.get_or_create(user=request.user)

    # Exclude posts created by the current user's profile
    posts = Post.objects.filter(user=user_profile)
    posts_count=posts.count()
    print(profile.count_following)
    return render(request,'userdetail/profile.html',{'profile':profile,
                                                     'posts':posts,
                                                     "posts_count":posts_count,
                                                     "followers":profile.count_following,
        "following":profile.count_followed_by,})
@login_required(login_url='userdetail:login')

def edit_profile(request, username):
    user = get_object_or_404(User, username=request.user.username)
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        profile_form = ProfileEditForm(request.POST,request.FILES, instance=profile)
        user_form=UpdateUserForm(request.POST,instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Updated")
            return redirect('post:home')
        else:
            messages.error(request,"Error")
    else:
        profile_form = ProfileEditForm(instance=profile)
        user_form=UpdateUserForm(instance=user)

    return render(request, 'userdetail/profile_edit.html', {'profile_form': profile_form,'user_form':user_form})

def user_profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
        profile = Profile.objects.get(user=user_profile)
    except (User.DoesNotExist, Profile.DoesNotExist):
        return render(request, 'userdetail/user_not_found.html')

    # Check if the logged-in user is following the current profile
    current_user_profile = Profile.objects.get(user=request.user)
    is_following = current_user_profile.is_following(profile)

    posts = Post.objects.filter(user=profile)
    posts_count = posts.count()

    context = {
        'user_profile': user_profile,
        'search_profile': user_profile,
        'profile': profile,
        'posts': posts,
        'posts_count': posts_count,
        'is_following': is_following,  # Pass the follow status dynamically
        'followers': profile.count_followed_by(),
        'following': profile.count_following(),
    }
    return render(request, 'userdetail/user_profile.html', context)

def follow_user(request, username): 
    user_to_follow = get_object_or_404(User, username=username)
    user_profile_to_follow = get_object_or_404(Profile, user=user_to_follow)
    current_user_profile = get_object_or_404(Profile, user=request.user)
    follow_user=True
    if current_user_profile.is_following(user_profile_to_follow):
        current_user_profile.unfollow(user_profile_to_follow)
        messages.success(request,"You have unfollowed")
        follow_user=False
        referer = request.META.get('HTTP_REFERER', '/')
        print(follow_user)
    else:
        current_user_profile.follow(user_profile_to_follow)
        messages.success(request,"You have followed")
        follow_user=True
        print(follow_user)
        referer = request.META.get('HTTP_REFERER', '/') # referer is used to redirect to that same page
    return redirect(referer)
    # return redirect(reverse(f"userdetail:user_profile",kwargs={"username":user_to_follow}))

#for searching custom user
def custom_profile(request,username):
    user_to_follow = get_object_or_404(User, username=username)
    user_profile_to_follow = get_object_or_404(Profile, user=user_to_follow)
    current_user_profile = get_object_or_404(Profile, user=request.user)
    context={'profile':current_user_profile}
    return render(request,'userdetail/user_profile',context)






