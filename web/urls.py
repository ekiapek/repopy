from django.urls import path
from web.views.web import home,code

urlpatterns = [
    path("", home.index, name="home"),
    path("code/",code.index, name="code")
]