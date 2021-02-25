class ResponseModel():
    def __init__(self,code,message):
        self.ResponseCode = code
        self.ResponseMessage = message

class SearchModel():
    def __init__(self,query,repoID):
        self.query = query
        self.repoID = repoID