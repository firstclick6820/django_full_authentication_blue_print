from django.urls import path



# import customs
from .views import HomePage

urlpatterns = [
    path('', HomePage, name="homePage")
]
