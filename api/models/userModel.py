from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.db import transaction
from .roleModel import *
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from .UploadMediaModel import UploadMedia
from django.conf import settings


# from django.contrib.auth.models import User as UserModel


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
 
    """
    # id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    wristband_id = models.CharField(max_length=250, blank=True, null=True)
    country_code = models.CharField(max_length=15, blank=True, null=True)
    phone_no = models.CharField(max_length=17, help_text='Contact phone number', blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True, help_text='Male, Female, Other')
    encoded_id = models.CharField(max_length=250, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True, help_text='1. Admin, 2. Sub Admin, 3. Student, 4. Administrator 5. Teachers, 6. AID, 7. Others')
    address = models.TextField(max_length=255, blank=True, null=True)
    longitude = models.TextField(max_length=80, blank=True, null=True)
    latitude = models.TextField(max_length=80, blank=True, null=True)
    profile_status = models.IntegerField(blank=True, null=True)
    image = models.ForeignKey(UploadMedia, on_delete=models.CASCADE, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    otp_varification = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_send_time = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    history = HistoricalRecords(table_name='user_history')

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'auth_user'
        indexes = [
            models.Index(fields=['id', 'first_name', 'last_name', 'email', 'is_active'])
        ]
