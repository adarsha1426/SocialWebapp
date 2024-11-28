from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name="post"
urlpatterns = [
    path('',views.home,name="home"),
    path('create',views.create_post,name="create_post"),
    path('post/<slug:post_slug>',views.postdetail,name="post"),
    path('like/<slug:post_slug>',views.like,name="like"),
    path('comment/<slug:post_slug>',views.create_comment,name="create_comment"),
    path('profile/<str:username>',views.postdetail,name="your_profile"),
    path('user_post/<slug:post_slug>',views.your_post,name="your_post"),
    path('delete_post/<slug:post_slug>',views.delete_post,name="delete_post"),
    path('delete/<slug:post_slug>',views.delete,name="delete"),
    path('share_email_form/<slug:post_slug>',views.share_form,name="share_email_form"),
    path('',include('userdetail.urls'),name="userdetail"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
