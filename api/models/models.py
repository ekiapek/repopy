from django.db import models
from datetime import datetime 

# Create your models here.
class Repositories(models.Model):
    RepositoryID = models.UUIDField(primary_key=True, max_length=40)
    RepositoryName = models.CharField(max_length=255,null=True)
    RepositoryBaseDir = models.TextField(null=True)
    ImportedDate = models.DateTimeField(null=True)
    LastIndexed = models.DateTimeField(null=True)

class Settings(models.Model):
    SettingID = models.UUIDField(primary_key=True, max_length=40)
    SettingKey = models.CharField(max_length=255,null=True)
    SettingValue = models.CharField(max_length=255,null=True)