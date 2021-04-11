from django.http.response import HttpResponseNotFound
from repopy.settings import API_URL
from django.shortcuts import render
from django.conf import settings
import requests as req
import jsons
# Create your views here.
def index(request, repositoryID):
    repoReq = req.get(API_URL+"repository/GetRepository/"+repositoryID)
    if(repoReq.status_code==200):
        resRepo = repoReq.json()
        if(resRepo != None):
            return render(request, "web/repository/main.html",{'repository':resRepo})
    return HttpResponseNotFound()