from api.models import Repositories, ApiModel
from django.http import HttpResponse,JsonResponse, response
import jsons
from repopy.settings import NO_REPOSITORY_FOUND, RESPONSE_ERROR,RESPONSE_SUCCESS

def getLatestIndexedRepository(request):
    # repositoryID = request.GET["RepositoryID"]
    try:
        repository = Repositories.objects.exclude(LastIndexed=None).order_by('-LastIndexed').first()
        if(repository != None):
            repoModel = ApiModel.Repositories()

            repoModel.RepositoryID = repository.RepositoryID
            repoModel.RepositoryName = repository.RepositoryName
            repoModel.RepositoryBaseDir = repository.RepositoryBaseDir
            repoModel.ImportedDate = repository.ImportedDate
            repoModel.LastIndexed = repository.LastIndexed

            responseModel = ApiModel.ResponseModel()
            responseModel.ResponseCode = RESPONSE_SUCCESS
            responseModel.ResponseMessage = "OK"
            responseModel.ResponseObject = jsons.dump(repoModel,cls=ApiModel.Repositories, strict=False)
            retrmodel = jsons.dump(responseModel)
            return JsonResponse(retrmodel,safe=False)
        else:
            responseModel = ApiModel.ResponseModel()
            responseModel.ResponseCode = NO_REPOSITORY_FOUND
            responseModel.ResponseMessage = "Repository Not Found"
            retrmodel = jsons.dump(responseModel)
            return JsonResponse(retrmodel,safe=False)
    except Exception as e:
        responseModel = ApiModel.ResponseModel()
        responseModel.ResponseCode = RESPONSE_ERROR
        responseModel.ResponseMessage = "Error getting repository"
        retrmodel = jsons.dump(responseModel)
        return JsonResponse(retrmodel,safe=False)