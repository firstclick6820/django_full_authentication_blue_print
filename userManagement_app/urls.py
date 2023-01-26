from django.urls import path
from django.contrib.auth import views as auth_views 

from .views import (
                     UserLogin, 
                     userRegister, 
                     userLogout, 
                     userVerifyEmail, 
                     user_password_reset, 
                     userProfile,
                     userPasswordResetComplete,
                     userProfileSettings)


urlpatterns = [
    
    path('login/', UserLogin, name="userLogin"),
    path('register/', userRegister, name='userRegister'),
    path('logout/', userLogout, name="userLogout" ),
    path('email_verify/', userVerifyEmail, name="userVerifyEmail"),
    path('password_reset/', user_password_reset, name="userPasswordReset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='userManagement_app/Auth/password/password_reset_done.html'),  name="passwordResetDone"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="userManagement_app/Auth/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', userPasswordResetComplete, name="userPasswordResetComplete"),  
    
    
    # Custom URL
    path('profile/<int:pk>/', userProfile, name="userProfile"), 
    path('settings/<int:pk>/', userProfileSettings, name='profileSettings')
]
