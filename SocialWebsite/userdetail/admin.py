from django.contrib import admin
from .models import Profile
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    # Specify the fields you want to display in the list view
    list_display = ['user','get_first_name','profile_pic','get_follower','get_following',]
    def get_follower(self,obj):
        return obj.count_followed_by()
    get_follower.short_description = "Followers"
    def get_first_name(self,obj):
        return obj.user.first_name
    get_first_name.short_description="First Name"
    def get_following(self,obj):
        return obj.count_following()
    get_following.short_description="Following"
admin.site.register(Profile, ProfileAdmin)