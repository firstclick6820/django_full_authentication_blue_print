from django.db import models

# Import AbstractUser class 
from django.contrib.auth.models import AbstractUser







# Define our Custom User Model
class User(AbstractUser):
    
    # STANDARD = 1
    # PREMIUM = 2
    # GOLD = 3
    
    # MEMBERSHIP_CHOICES = (
    #     (STANDARD, 'Standard'),
    #     (PREMIUM, 'Premium'),
    #     (GOLD, 'Gold')
    # )
    
    ACCOUNT_TYPE_CHOICES = [
        ('creator', 'Creator'),
        ('supporter', 'Supporter'),
    ]
    
    # This is required while we are limiting users to access the password reset done page.
    has_recently_reset_password = models.BooleanField(default=False)
    
    # Add is_active if the user not varified their email
    is_email_verified = models.BooleanField(default=False)
 
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)

    # By Default Django Uses Username, we give the Email Login Functionality
    email = models.EmailField(unique=True, max_length=100)
    verification_token = models.CharField(max_length=255)
    # Add User Memebership
    # membership = models.CharField(choices=MEMBERSHIP_CHOICES, default=STANDARD, max_length=1)
    
    
    
    
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
    
    
    

    
    