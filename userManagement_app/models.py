from django.db import models
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
    
 
    # By Default Django Uses Username, we give the Email Login Functionality
    email = models.EmailField(unique=True, max_length=100)
    
    # Add User Memebership
    # membership = models.CharField(choices=MEMBERSHIP_CHOICES, default=STANDARD, max_length=1)
    
    def __str__(self):
        return self.email

  
    
    
    
# Creating Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    bio = models.CharField(max_length=100, blank=True, null=True)
    summary = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    
    
    
    
    #Return the user Email, khalid@mgail.com
    def __str__(self):
        return self.user.email
    
    
    

    
    