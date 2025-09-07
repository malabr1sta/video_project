from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model to handle user and superuser creation.
    """

    def create_user(self, username, password, **extra_fields):
        """
        Create and save a regular user with the given username and password.

        Args:
            username (str): The username for the user.
            password (str): The password for the user.
            **extra_fields: Additional fields for the user model.

        Raises:
            ValueError: If the username is not provided.

        Returns:
            User: The created user instance.
        """
        if not username:
            raise ValueError(_("The Username must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a superuser with the given username and password.

        Args:
            username (str): The username for the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the user model.

        Raises:
            ValueError: If is_staff or is_superuser is not True.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)


