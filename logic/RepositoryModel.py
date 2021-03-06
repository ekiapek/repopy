class RepositoryModel:
    def __init__(self):
        self.RepositoryName = None
        self.BasePath = None
        self.Documents = []

class DocumentModel:
    def __init__(self):
        self.DocumentName = None
        self.DocumentPath = None
        self.Imports = []
        self.Classes = []

class ClassModel:
    def __init__(self):
        self.Name = None
        self.Type = None
        self.LineNo = None
        self.ColOffset = None
        self.Parents = []

class ParentClassModel:
    def __init__(self):
        self.Name = None
        self.Type = None

class IndexedRepositoryModel:
    def __init__(self):
        self.RediSearchClient = None
        self.RedisGraphClient = None

class ImportModuleModel:
    def __init__(self):
        self.ModulePackageName = None
        self.ModuleName = None
        self.ModuleAliasName = None