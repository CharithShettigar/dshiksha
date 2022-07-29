from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.utils import timezone

# Create your models here.
class UserTypes(models.Model):
    UserTypeID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UserTypeName = models.CharField(max_length=50)
    OrderNo = models.IntegerField()
    # def __str__(self):
    #     return self.UserTypeName


class UserManager(BaseUserManager):
    def create_superuser(self, Email, FirstName, username, password, UserType, **other_fields):
        other_fields.setdefault('IsActive', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)  

        if other_fields.get('is_superuser') is not True:
            raise ValueError("Super User must be assigned")
        
        return self.create_user(email = Email, first_name = FirstName, username = username, password = password, UserType = UserType, **other_fields)

    def create_user(self, email, first_name, username, password, UserType, **other_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(Email = email, FirstName = first_name, username = username, UserType = UserTypes.objects.get(UserTypeID = UserType), **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    UserID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Email = models.EmailField(max_length=255, unique=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50, null=True, default='')
    StartDate = models.DateTimeField(default=timezone.now)
    LastLogin = models.DateTimeField(auto_now=True)
    IsActive = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)
    UserType = models.ForeignKey(UserTypes, on_delete=models.CASCADE)

    objects = UserManager()
    
    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['FirstName', 'username', 'UserType']

    def __str__(self):
        return self.Email
