from django.urls import path


from .views import getRecentPolls, getAPoll, votePoll, createAPoll


urlpatterns = [
    path('', getRecentPolls, name='getRecentPolls'),
    path('<int:pk>/', getAPoll, name="getAPoll"),
    path('vote/<int:question_pk>/', votePoll, name="votePoll"),
    path('create/', createAPoll, name='createAPoll')
    
]
