from django.urls import path,include
from web import views
from api.views import search,indexing

urlpatterns = [
    path(r'searchSuggest/', search.searchSuggest),
    path(r'indexer/', indexing.indexer)
]