"""Auth application admin registration."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
