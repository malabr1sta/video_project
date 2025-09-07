# pyright: reportArgumentType=false, reportIncompatibleVariableOverride=false
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts import managers as accounts_managers


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using username as the unique identifier.

    Attributes:
        username: Unique username for the user.
        is_active: Designates whether this user account is active.
        is_staff: Designates whether the user can access the admin site.

    Class Attributes:
        USERNAME_FIELD: Field used for authentication.
        REQUIRED_FIELDS: List of required fields besides USERNAME_FIELD.
        objects: Custom manager for user creation and management.
    """

    username = models.CharField(max_length=150, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = accounts_managers.CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

