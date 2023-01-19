from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

import uuid


from .forms import CustomUserCreationForm
User = get_user_model()










# This funcation is used to send a uique verification token to the user to verify their email
def generate_verification_token(user):
    return '{}-{}'.format(user.email, str(uuid.uuid4()))



# ////////////////////////////////////////////////////////////////////////////// USER LOGIN  //////////////////////////////////
# User Login Funcation
def UserLogin(request):
    
    # check if the user is already logged in, send them back to home page
    if request.user.is_authenticated:
        messages.add_message(request, messages.SUCCESS,"You have already Logged in!")
        return redirect('homePage')
    
    
    
    # check if the request is a post method
    if request.method == 'POST':
        
        # Grap username, email, and password
        
        email  = request.POST['email']
        password = request.POST['password']
        
        
        user = authenticate(email=email, password=password)
        
        # check if the user already exists in the database.
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You have logged in successfully!')
            return redirect('homePage')
        else:
            messages.add_message(request, messages.WARNING, 'Wrong Cordentials, please try again!')
            return redirect('userLogin')
    else:
        return render(request, 'userManagement_app/Auth/login.html')



# ////////////////////////////////////////////////////////////////////////////// USER REGISTERATION ////////////////////////////
# User Registeration
def userRegister(request):
    # check if the user is already logged in, send them back to home page.
    if request.user.is_authenticated:
        messages.add_message(request, messages.SUCCESS,"You have already Logged in!")
        return redirect('userLogin')
    
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            
            # Grap the username and password for logging user

            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            user = authenticate(email=email, password=password)
            
            # Once the user is registered now let's send them a verification email
            token = generate_verification_token(user)
            user.verification_token = token
            
            user.save()

  
            
            subject = "Verify Your Email"
            email_template_name = "userManagement_app/Auth/patterns/email_verification_email.txt"
            c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'MKM IT SOLUTION',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
                    'name':user.username ,
					'protocol': 'http',
                    'link': 'http://localhost:8000/accounts/email_verify?token={}'.format(token)
					}
                    
                    
            email = render_to_string(email_template_name, c)
            send_mail(subject, email, 'mohammadkhalidmomand@gmail.com' , [user.email], fail_silently=False)
            

            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Your account created Successfully.')
            return redirect('homePage')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong, try again!')
            return redirect('userLogin')
    else:
        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, 'userManagement_app/Auth/register.html', context)


# ////////////////////////////////////////////////////////////////////////////// USER LOGOUT //////////////////////////////////
@login_required
def userLogout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "You have logged out successfully.")
    return redirect('homePage')


    
# ////////////////////////////////////////////////////////////////////////////// VERIFY EMAIL //////////////////////////////////   
@login_required 
# User Email Verification
def userVerifyEmail(request):
    
    # Grap the token send to the user email
    token = request.GET.get('token')
    
    # Retrieve the user with the matching token
    user = get_object_or_404(User, verification_token=token)

    if user:
        user.is_email_verified = True
        user.save()
        
        return render(request, 'userManagement_app/Auth/userVerifyEmail.html', {"verify": True})
    
    return render(request, 'userManagement_app/Auth/userVerifyEmail.html', {"verify": False})



# ////////////////////////////////////////////////////////////////////////////// PASSWORD RESET  /////////////////////////////////
def user_password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        
        if password_reset_form.is_valid():
            
            data = password_reset_form.cleaned_data['email']
            
            associated_users = User.objects.filter(Q(email=data))
            
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "userManagement_app/Auth/patterns/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'MKM IT SOLUTION',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    
                    email = render_to_string(email_template_name, c)
                    
                    try:
                        send_mail(subject, email, 'mohammadkhalidmomand@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("passwordResetDone")
                
    passwordResetForm = PasswordResetForm()
    return render(request=request, template_name="userManagement_app/Auth/password/password_reset.html", context={"passwordResetForm":passwordResetForm})



# ////////////////////////////////////////////////////////////////////////////// CHANGE PASSWORD  ////////////////////////////////