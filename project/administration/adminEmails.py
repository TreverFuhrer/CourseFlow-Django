from django import forms
from .models import adminEmail

class EmailMessage(forms.ModelForm):
    class Meta:
        model = adminEmail
        fields = ['email', 'subject', 'message']
