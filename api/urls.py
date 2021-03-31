from django.urls import path,include
from web import views
from api.views import files, search,indexing

urlpatterns = [
    path(r'search/SearchSuggest/', search.searchSuggest),
    path(r'indexing/IndexRepoDirectory/', indexing.indexRepoDirectory),
    path(r'indexing/IndexRepo/', indexing.indexRepo),
    path(r'indexing/UploadRepository/', indexing.repoUpload),
    path(r'files/Get/', files.getFile)
]