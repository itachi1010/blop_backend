from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


admin.site.register(User, UserAdmin)
admin.site.register(CustomUser)
