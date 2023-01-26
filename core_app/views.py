from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Q

from polls_app.models import Poll



User = get_user_model()


def HomePage(request):
    polls = Poll.objects.filter(created_by__account_type='creator', created_by__is_email_verified=True, is_published=True, is_active=True ).order_by('-created_at')
    users = User.objects.filter(is_email_verified=True)
    # by default user_type is assigned to visitor 
    user_type = 'visitor'
    
    # if a user is authenticated then check the user type
    if request.user.is_authenticated:
        user_type = request.user.account_type
       
        

    
    
    context = {"polls": polls, 'user_type': user_type, 'users': users}
    return render(request, 'core_app/home.html', context )