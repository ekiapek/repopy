from django.http.response import JsonResponse
import jsons
from repopy.settings import NO_REPOSITORY_FOUND, RESPONSE_ERROR, RESPONSE_SUCCESS
from api.models import ApiModel
from api.models.models import FileModel, Repositories
import uuid
from django.http import FileResponse
import pathlib
from django.views.decorators.cache import cache_page

@cache_page(60*15)
def getFile(request):
    if(request.GET['FileID'])!=None:
        file = FileModel.objects.get(FileID = request.GET['FileID'])
        fileResponse = open(file.FilePath,"rb")
        return FileResponse(fileResponse)

# @cache_page(60*15)
def getFilesInRepo(request):
    try:
        repoID = uuid.UUID(request.GET['RepositoryID'])
        repository = Repositories.objects.get(RepositoryID=repoID)
        if(repository != None):
            baseDir = repository.RepositoryBaseDir
            filesInRepoList = FileModel.objects.filter(RepositoryID = repository.RepositoryID)
            fileList = []
            for f in pathlib.Path(baseDir).glob('**/*'):
                file = filesInRepoList.filter(FilePath = f).first()
                if(file != None):
                    fileNode = ApiModel.FileNodeModel()
                    fileNode.id = file.FileID
                    fileNode.text = file.Filename

                    parent = filesInRepoList.filter(FilePath = f.parent).first()
                    if(parent != None):
                        fileNode.parent = parent.FileID
                    else:
                        fileNode.parent = "#"

                    if(f.is_dir()):
                        fileNode.icon = "bi bi-folder"
                    else:
                        fileNode.icon = "bi bi-file-earmark"
                    
                    fileList.append(fileNode)

            # responseModel = ApiModel.ResponseModel()
            # responseModel.ResponseCode = RESPONSE_SUCCESS
            # responseModel.ResponseMessage = "OK"
            # responseModel.ResponseObject = jsons.dump(fileList,strict=False)
            retrmodel = jsons.dump(fileList)
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
