from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# for email
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from SocialWebsite.settings import EMAIL_HOST_USER
from userdetail.models import Profile

from post.forms import CommentForm, PostForm
from post.models import Comment, Post, Repost

from .forms import ShareEmailForm


# Create your views here.
@login_required(login_url="userdetail:login")
def home(request):
    current_user = request.user
    user_profile = get_object_or_404(
        Profile, user=current_user
    )  # logged in user profile

    posts = Post.objects.exclude(user=user_profile)
    # Fetching full model instances instead of values()
    suggested_user_profile = Profile.objects.exclude(user=current_user)
    suggested_user = User.objects.exclude(
        id=current_user.id
    )  # this is for post of user profile

    reposted_post_ids = Repost.objects.filter(user=user_profile).values_list(
        "post_id", flat=True
    )
    print(reposted_post_ids)
    context = {
        "posts": posts,
        "suggested_user": suggested_user,
        "user_profile": user_profile,
        "comment_count": user_profile,
        "reposted_post_ids": reposted_post_ids,
        "flag": flag,
    }

    return render(request, "post/homepage.html", context)


def flag(request):
    pass


# nav bar
def base(request):
    user = get_object_or_404(User, username=request.user)
    profile = Profile.objects.get(user=request.user)
    return render(request, "base.html", {"current_profile": profile})


# creating post
@login_required
def create_post(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(
            user=request.user
        )  # Get the Profile of the logged-in user
        if request.method == "POST":
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)  # Don't save to the database yet
                post.user = profile  # Assign the Profile, not the User
                post.save()  # Now save the post
                messages.success(request, "Post created successfully!")
                return redirect("post:home")  # Redirect after successful post creation
            else:
                messages.error(request, "Error while posting form")
        else:
            post_form = PostForm()
    else:
        return redirect("post:home")
    return render(
        request,
        "post/create_post.html",
        {"post_form": post_form, "user_profile": profile},
    )


# post detail
def postdetail(request, post_slug):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Post, slug=post_slug)
    print("Post User", post.user)
    comments = Comment.objects.filter(post=post)
    comment_count_queryset = Comment.objects.annotate(Count("body")).filter(post=post)
    comment_count = len(comment_count_queryset)
    return render(
        request,
        "post/post.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "user_profile": profile,
        },
    )


# post like
def like(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    msg = False
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
        msg = False

    else:
        post.likes.add(request.user.profile)
        msg = True

    like_count = post.count_like()
    referer = request.META.get(
        "HTTP_REFERER", "/"
    )  # referer is used to redirect to that same page
    return redirect(referer)


# Creating comment
@login_required
def create_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = (
                request.user.profile
            )  # Assuming comments are linked to a user
            comment.save()
            return redirect("post:home")  # Redirect after successful comment
    else:
        form = CommentForm()
    return render(
        request, "post/create_comment.html", {"comment_form": form, "post": post}
    )


def your_post(request, id):
    user = request.user
    profile = get_object_or_404(Profile, user=user)  # Get the profile based on the user

    posts = Post.objects.filter(user=profile)
    comment = Comment.objects.get(post=posts)
    return render(request, "post/your_post.html", {"posts": posts, "comment": comment})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user.user == request.user:
        post.delete()
        return redirect("post:home")
    else:
        return HttpResponse(request, "Error")


def delete(request, post_slug):
    post = get_object_or_404(Post, id=post_slug)
    if post.user.user == request.user:
        return render(request, "post/delete_post.html", {"post": post})
    else:
        return HttpResponse(
            f"{request.user} Post user {post.user.user}You are not authorized to delete this post."
        )


@login_required
def share_form(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    sent = False
    form = ShareEmailForm()
    if request.method == "POST":
        form = ShareEmailForm(request.POST)
        if form.is_valid():
            post_url = request.build_absolute_uri(post.get_sharedpost_url())
            name = f"{request.user}"
            to = form.cleaned_data["to"]
            comment = form.cleaned_data["message"]
            message = (
                f"This post was shared by your friend {request.user.username}.\n\n"
                f"Post URL: {post_url}\n\n"
                f"Message: {comment}"
            )
            subject = "Social web app post share via email"
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                [to],
                fail_silently=False,  # Raise exceptions if email fails
            )

            referer = request.META.get(
                "HTTP_REFERER", "/"
            )  # referer is used to redirect to that same page
            return redirect(referer)
        success_message = "Email not sent"
    return render(
        request,
        "post/share_email_form.html",
        {
            "form": form,
            "post": post,
        },
    )


def repost(request, post_slug):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Post, slug=post_slug)
    repost, created = Repost.objects.get_or_create(user=profile, post=post)
    if created:
        messages.success(
            request, f"{post.id} is reposted by user {profile.user.first_name}"
        )
    else:
        repost.delete()
        messages.info(
            request, f"{post.id} is DELTED reposted by user {profile.user.first_name}"
        )
    return redirect("post:home")
