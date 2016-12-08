from __future__ import unicode_literals

from django.db import models
from django.contrib import auth

class user(auth.models.AbstractBaseUser, auth.models.PermissionsMixin):
    USERNAME_FIELD = 'username'

    username = models.CharField(max_length=256, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = auth.models.UserManager()

    def get_long_name(self):
        return self.username

    def get_short_name(self):
        return self.get_long_name()

    def get_url(self):
		return '/'
		
