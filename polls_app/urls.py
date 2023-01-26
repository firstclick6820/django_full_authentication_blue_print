from django.urls import path


from .views import getRecentPolls, getAPoll, votePoll


urlpatterns = [
    path('', getRecentPolls, name='getRecentPolls'),
    path('<int:pk>/', getAPoll, name="getAPoll"),
    path('vote/<int:question_pk>/', votePoll, name="votePoll"),
    
]
