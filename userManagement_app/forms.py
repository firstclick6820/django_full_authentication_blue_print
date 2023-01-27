from django.contrib.auth.forms  import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError  
from django import forms
from django.contrib.auth.forms import PasswordResetForm


from django.contrib.auth import get_user_model

from .models import Profile



User = get_user_model()




#///////////////////////////////////////////////////////////// REGISTRATION FORM  /////////////////////////////////////////
class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(label='Email')
    ACCOUNT_TYPE_CHOICES = [
        ('creator', 'I am a content Creator'),
        ('supporter', 'I want to follow and vote'),
    ]
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE_CHOICES, widget=forms.RadioSelect())
    
    class Meta:
        model =  get_user_model()
        fields = ('email', 'password1', 'password2', 'account_type')
        exclude = ('username',)
        labels = {
            'password1': 'Password',
            'password2': 'Confirm Password'
        }
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }
        
  
    
    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError('Email Already Exists!')
        return email
    
        
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        
        if password1 and password2 and password1 !=password2:
            raise ValidationError("Passwords don't match!")
        return password2
    
    def save(self, commit = True):
        account_type = self.cleaned_data['account_type'] 
          
        user = User.objects.create_user(   
            self.cleaned_data['email'],  
            self.cleaned_data['password1'],
            
        ) 
        user.account_type = account_type 
        Profile.objects.create(user=user)
        user.save()
        return user
        
        
        
        
#///////////////////////////////////////////////////////////// LOGIN FORM /////////////////////////////////////////       
class LoginForm(AuthenticationForm):
    
    username = forms.CharField(label='Email / Username')




# /////////////////////////////////////////////////////////////PASSWORD RESET FORM ///////////////////////////////


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

