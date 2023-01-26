from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Poll(models.Model):
    question = models.CharField(max_length=255)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def total_votes(self):
        choices = self.choices.all()
        if choices:
            total_votes = sum(choice.votes for choice in choices)
            return int(total_votes)
        return 0

    
    
    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    
    
    class Meta:
        unique_together = ('question', 'choice_text')
    
    def vote_percentage(self):
        total_votes = sum(choice.votes for choice in self.question.choices.all())
        if total_votes:
            return int((self.votes / total_votes) * 100)
        return 0

    def __str__(self):
        return self.choice_text




class Vote(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    vote_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.user.username
    
    


