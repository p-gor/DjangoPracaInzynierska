from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Account
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Register your models here.


admin.site.register(Profile)
admin.site.register(Account)
