from django.shortcuts import render



def HomePage(request):
    return render(request, 'core_app/home.html', {})