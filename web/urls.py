from django.urls import path
from web.views.web import home,code,welcome

urlpatterns = [
    path("", home.index, name="home"),
    path("code/",code.index, name="code"),
    path("welcome/", welcome.index, name="welcome"),
    path("welcome/create-repo/", welcome.create_repo, name="create-repo")
]