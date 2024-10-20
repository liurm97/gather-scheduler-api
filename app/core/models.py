from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        try:
            if not email:
                raise ValueError("Email address must be provided")
            # validate email input provided by user
            validate_email(email)
            # if validated
            # normalize and set user email, extra_fields(optional)
            user = self.model(email=self.normalize_email(email),
                              **extra_fields)
            # calls `make_password` to hash/salt the password before saving
            user.set_password(password)
            # save user record into db
            user.save(using=self._db)
            # return user record
            return user
        except ValidationError:
            # if not validated, return error message
            return {"message": "Email address is not the right format"}

    def create_superuser(self, email, password=None, **extra_fields):
        """Create superuser"""
        # normalize and set user email, extra_fields(optional)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # set supervisor to True
        user.is_superuser = True
        # set staff to True
        user.is_staff = True
        # encrypy and set user password
        user.set_password(password)
        # save user record into db
        user.save(using=self._db)
        # return user record
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Define User model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # Use "email" field for user authentication
    # instead of the default "username" field
    USERNAME_FIELD = "email"
