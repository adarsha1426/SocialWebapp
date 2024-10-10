from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    # Specify the fields you want to display in the list view
    list_display = ['user','get_first_name','profile_pic']
    def get_first_name(self,obj):
        return obj.user.first_name
    get_first_name.short_description="First Name"
admin.site.register(Profile, ProfileAdmin)