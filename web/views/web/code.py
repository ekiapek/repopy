from django.shortcuts import render
from django.http import HttpResponse
import re
# Create your views here.
def index(request):
    return render(request, "web/code/main.html")