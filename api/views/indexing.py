from django import conf
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.http.response import HttpResponseNotAllowed, HttpResponseServerError
from api.models.ApiModel import ResponseModel,RepositoryIndexRequestModel,ErrorModel
from django.conf import settings
from logic import parser
from logic import indexer as idx
import jsons
import logging
import traceback

redis = settings.REDIS_INSTANCE
def indexer(request):
    if (request.method == "POST"):
        if(request.POST != None):
            repoModel = jsons.loads(request.body,RepositoryIndexRequestModel)
            try:
                parsedRepo = parser.parseCode(repoModel.RepositoryPath,repoModel.RepositoryName)
                indexedRepo = idx.indexRepo(parsedRepo,redis)
                retrmodel = jsons.dump(parsedRepo)
                return JsonResponse(retrmodel,safe=False)
            except Exception as e:
                errmsg = traceback.format_exc(limit=1)
                tb = traceback.format_tb(e.__traceback__)
                err = ErrorModel(msg=errmsg, trace=tb,module="Indexer")
                retrmodelerr = jsons.dump(err)
                print(retrmodelerr)
                return HttpResponseServerError()
                # return JsonResponse(retrmodelerr,safe=False)

    else:
        return HttpResponseNotAllowed("Not Allowed!")
