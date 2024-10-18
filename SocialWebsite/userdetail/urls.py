from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='userdetail'
urlpatterns = [

    path('login',views.login_view, name="login"),
    path('register',views.register, name="register"),
    path('logout',views.logout_view,name="logout"),
    path('change',views.change_password,name='change'),
    path('profile',views.profile,name='profile'),
    path('user_profile/<str:username>',views.user_profile,name="user_profile"),
    path('custom_profile/<str:username>',views.custom_profile,name="custom_search_profile"),
    path('follow/<str:username>',views.follow_user,name='follow_user'),
    path('edit_profile/<str:username>',views.edit_profile,name='edit'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)