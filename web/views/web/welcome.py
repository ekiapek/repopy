from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "web/welcome/welcome.html")

def create_repo(request):
    return render(request, "web/welcome/create.html")