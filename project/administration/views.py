from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
def home(request):
    return render(request, 'home.html')