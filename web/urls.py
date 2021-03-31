from django.urls import path
from web.views.web import home,repository,welcome

urlpatterns = [
    path("", home.index, name="home"),
    path("repository/<str:repositoryID>/",repository.index, name="repository"),
    path("welcome/", welcome.index, name="welcome"),
    path("welcome/create-repo/", welcome.create_repo, name="create-repo")
]