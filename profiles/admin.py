from django.contrib import admin
from profiles.models import UserProfile, GroupProfile


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['user']
   


class GroupProfileAdmin(admin.ModelAdmin):
    model = GroupProfile
    list_display = ['group']
   

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GroupProfile, GroupProfileAdmin)

