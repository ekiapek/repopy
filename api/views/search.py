from django.http import HttpResponse,JsonResponse
from django.conf import settings
import os
from redisearch import *
import redisearch.aggregation as aggregations
import redisearch.reducers as reducers
from api.models.ApiModel import ResponseModel

redis_instance = settings.REDIS_INSTANCE
client = None

def searchSuggest(request):
    words = []
    headline1 = []
    headline2 = []
    response = {}
    queryString = ""
    repo = ""

    if request.method == 'GET' and 'q' in request.GET:
        queryString = request.GET['q']

    # if request.method == 'GET' and 'repo' in request.GET:
    #     repo = request.GET['repo']
    
    # result = Query(queryString).with_scores()
    queryString = queryString.lower()
    queryString = queryString.split()

    for qstr in queryString:
        word = {'name':qstr}
        words.append(word)
    #     headline1.append(word)
    #     headline2.append(word)  
    # 

    response["words"] = words

    if "burger" in queryString:
        headline1 = []
        headline2 = []
        a = {'name':"Burger"}
        b = {'name':"CheeseBurger"}
        headline1.append(a)
        headline2.append(b)
        response["suggests"] = {"Class":headline1,"Child": headline2}
    
    if "cheese" in queryString:
        a = {'name':"Burger"}
        b = {'name':"CheeseBurger"}
        headline1 = []
        headline2 = []
        headline1.append(b)
        headline2.append(a)
        response["suggests"] = {"Class":headline1,"Parent": headline2}

    if "cheeseburger" in queryString:
        headline1 = []
        headline2 = []
        a = {'name':"Burger"}
        b = {'name':"CheeseBurger"}
        headline1.append(b)
        headline2.append(a)
        response["suggests"] = {"Class":headline1,"Parent": headline2}

    if "parent" in queryString:
        if any("cheese" in s for s in queryString):
            headline1 = []
            headline2 = []
            a = {'name':"Burger"}
            b = {'name':"CheeseBurger"}
            headline1.append(a)
            headline2.append(b)
            response["suggests"] = {"Parent":headline1,"Class": headline2}

    return JsonResponse(response)

def selectRepo(request):
    if request.method == 'POST' and 'repository' in request.POST:
        repo = request.POST['repository']
        if client == None:
            client = Client(repo,conn=redis_instance)
            response = ResponseModel(code=00,message="Success")
            return JsonResponse(response)
        else:
            client.index_name = repo
            response = ResponseModel(code=00,message="Success")
            return JsonResponse(response)

