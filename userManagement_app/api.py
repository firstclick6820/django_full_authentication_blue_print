from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse



# Restframework Models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser



# Import Custom User
from django.contrib.auth import get_user_model
User = get_user_model()






# ====================== User API  =========================================

# Check whether the email address is taken or not
@api_view(['GET'])
def CheckEmailAPI(request, email):
    is_email_avialable = User.objects.filter(email=email).exists()
    
    if is_email_avialable:
        return JsonResponse({'available': False}, safe=False)
    else:
        return JsonResponse({'available': True}, safe=False)
