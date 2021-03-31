from datetime import datetime
import pytz
from django import forms

class ResponseModel():
    def __init__(self):
        self.ResponseCode = None
        self.ResponseMessage = None

class SearchModel():
    def __init__(self,query,repoID):
        self.query = query
        self.repoID = repoID

class RepositoryIndexRequestModel(object):
    def __init__(self):
        self.RepositoryName = None
        self.RepositoryPath = None

class ErrorModel:
    def __init__(self,msg = None, trace = None, module = None):
        self.ErrMsg = msg
        self.Trace = trace
        self.Module = module
        self.Created = datetime.now(tz=pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S")