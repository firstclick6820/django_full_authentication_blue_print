from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)





class User(AbstractBaseUser, PermissionsMixin):
    
    objects = UserManager()
    
    ACCOUNT_TYPE_CHOICES = [
        ('creator', 'Creator'),
        ('supporter', 'Supporter'),
    ]
    
    
    # This is required while we are limiting users to access the password reset done page.
    has_recently_reset_password = models.BooleanField(default=False)
    
    
    # Add is_active if the user not varified their email
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
 
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)


    # By Default Django Uses Username, we give the Email Login Functionality
    email = models.EmailField(unique=True, max_length=100)
    
    verification_token = models.CharField(max_length=255)
  
    username = None
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['account_type']

    
    
    
    def reset_password(self):
        # your code to reset password
        self.has_recently_reset_password = True
        self.save()




    def __str__(self):
        return self.email

  
    
    
    
# Creating Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    bio = models.CharField(max_length=100, blank=True, null=True)
    summary = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address=models.CharField(max_length=255, blank=True, null=True)
    
    
    
    
    
    #Return the user Email, khalid@mgail.com
    def __str__(self):
        return self.user.email
    
    
    

    
    