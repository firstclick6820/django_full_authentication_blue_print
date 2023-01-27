from django.urls import path


from .api import CheckEmailAPI

urlpatterns = [
    path('check_email/<str:email>/', CheckEmailAPI, name="checkEmailAAPI")
]