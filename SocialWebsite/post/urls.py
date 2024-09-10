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


    path('',include('userdetail.urls'),name="userdetail"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
