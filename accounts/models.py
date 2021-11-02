from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, UserManager)

# How to create a custom authentication system
# https://betterprogramming.pub/how-to-create-a-custom-authentication-system-in-django-24868f65ac53


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', unique=True)
    first_name = models.CharField(verbose_name='first name')
    last_name = models.CharField(verbose_name='last name')
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'is_admin']

    def __str__(self):
        return self.email + "\n" + self.first_name + " " + self.last_name

    def has_admin_perm(self, perm, obj=None):
        """
        Does the user have admin permissions?
        """
        return self.is_admin


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
