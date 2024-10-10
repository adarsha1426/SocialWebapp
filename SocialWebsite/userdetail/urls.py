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
    path('edit_profile/<str:username>',views.edit_profile,name='edit'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)