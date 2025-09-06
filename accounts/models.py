# pyright: reportArgumentType=false, reportIncompatibleVariableOverride=false
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts import managers as accounts_managers


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = accounts_managers.CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

