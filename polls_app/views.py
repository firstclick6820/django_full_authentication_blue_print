from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import user_passes_test, login_required

from django.shortcuts import render, redirect, get_object_or_404

from .models import Poll, Choice, Vote










# Create your views here.
def getRecentPolls(request):
    polls = Poll.objects.filter(created_by__account_type='creator', created_by__is_email_verified=True, is_published=True, is_active=True ).order_by('-created_at')
    user = request.user
    
    for poll in polls:
        if user in poll.votes.all():
            return HttpResponse('IT is there')

    context = {"polls": polls, 'user': user}      
    return render(request, 'polls_app/getRecentPolls.html', context)



# Get A Specific Poll by its ID
def getAPoll(request, pk):
    poll = Poll.objects.get(id=pk)
    
    # check if the user  is logged
    if request.user.is_authenticated:
        vote_exists = Vote.objects.filter(question=poll,user=request.user).exists()
    else:
        vote_exists = False
    
    context={"poll": poll, 'vote_exists': vote_exists}
    return render(request, 'polls_app/getAPoll.html', context)



# Create A Poll
def createAPoll(request):
    return render(request, 'polls_app/createAPoll.html', {})



@login_required
def votePoll(request, question_pk):
    poll = Poll.objects.get(id=question_pk)
    user = request.user
    vote_exists = Vote.objects.filter(question=poll,user=request.user).exists()
    
    
    if vote_exists:
        context={"poll": poll, 'vote_exists': vote_exists}
        return render(request, 'polls_app/getAPoll.html', context)
    
    
    # Check if the request is a post request. means a user has sent the vote.
    if request.method == "POST":
        # find out the selected choice that a user has selected to vote.
        selected_choice = poll.choices.get(pk=request.POST['choice'])
        # add a vote for a selected choice.
        selected_choice.votes += 1
        # save the vote in the database.
        selected_choice.save()
        
        
        # create a vote instance for the future to check who has voted for which choice and question.
        vote = Vote.objects.create(question=poll, choice=selected_choice, user=user, ip_address=request.META['REMOTE_ADDR'])
        vote.save()
        
        # return a user to the getAPoll page with a result.
        vote_exists = Vote.objects.filter(question=poll,user=request.user).exists()
        context={"poll": poll, 'vote_exists': vote_exists}
        return render(request, 'polls_app/getAPoll.html', context)
        

    context= {"poll": poll}
    return render(request, 'polls_app/getAPoll.html', context)
    
    
