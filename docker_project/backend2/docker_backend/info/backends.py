from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from .models import CustomUser

class CustomUserBackend:
    def authenticate(self, request, name=None, password=None, **kwargs):
        try:
            users = CustomUser.objects.filter(name=name)
            if len(users) > 0:
                user = users[0]
                if user.check_password(password):
                    return user
            else:
                return None
        except CustomUser.DoesNotExist:
            return None
