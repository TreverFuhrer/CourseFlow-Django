from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages') #change to student Email
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

