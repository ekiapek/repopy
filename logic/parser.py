from os.path import basename
import astroid
import glob
from logic.RepositoryModel import ClassModel,RepositoryModel,ParentClassModel,DocumentModel
import os
import jsonpickle

def parseCode(base_dir,repository_name):
    # root_dir needs a trailing slash (i.e. /root/dir/)
    repo = RepositoryModel()
    repo.RepositoryName = repository_name
    repo.BasePath = base_dir

    for filename in glob.iglob(base_dir + '**/*.py', recursive=True):
        file = open(filename).read()
        code = astroid.parse(file)
        document = DocumentModel()
        document.DocumentPath = filename
        document.DocumentName = os.path.basename(filename)

        for node in code.body:
            if(isinstance(node,astroid.ClassDef)):
                # print("\n"+filename)
                classNode = ClassModel()
                classNode.Name = node.name
                classNode.LineNo = node.blockstart_tolineno
                classNode.ColOffset = node.col_offset
                classNode.Type = node.type

                if(len(node.bases)>0):
                    # print(node.name+" line: "+str(node.blockstart_tolineno)+" col: "+str(node.col_offset)+" Parent: ")
                    for base in node.bases:
                        if(isinstance(base,astroid.Attribute)):
                            attrNode = ParentClassModel()
                            attrNode.Name = base.attrname
                            attrNode.Type = "attribute"
                            classNode.Parents.append(attrNode)
                            # print(base.attrname+" col: "+str(base.col_offset))
                        elif(isinstance(base,astroid.Call)):
                            funcNode = ParentClassModel()
                            funcNode.Name = base.func.name
                            funcNode.Type = "function"
                            classNode.Parents.append(funcNode)
                        else:
                            parentNode = ParentClassModel()
                            parentNode.Name = base.name
                            parentNode.Type = "class"
                            classNode.Parents.append(parentNode)
                
                document.Classes.append(classNode)
        
        repo.Documents.append(document)
    
    return repo