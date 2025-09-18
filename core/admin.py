from django.contrib import admin

from core.models import UserGroup


# Register your models here.

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ["id","user_id","group_id"]