from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name="post"
urlpatterns = [
    path('',views.home,name="home"),
    path('create/',views.create_post,name="create_post"),
]
