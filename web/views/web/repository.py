from django.shortcuts import render
from django.http import HttpResponse
import re
# Create your views here.
def index(request, repositoryID):
    return render(request, "web/repository/main.html")