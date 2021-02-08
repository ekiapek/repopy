from django.urls import path,include
from web import views
from api.views import search

urlpatterns = [
    path(r'searchSuggest/', search.searchSuggest)
]