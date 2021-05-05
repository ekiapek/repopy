import pathlib
from redisearch import Client,IndexDefinition,TextField,AutoCompleter
from redisgraph import Node, Edge, Graph
from logic.RepositoryModel import IndexedRepositoryModel
from api.models.models import FileModel

def indexRepo(repo=None, redisConn=None):
    """
    do indexing on repository object with redisConn connection
    """
    if(repo != None):
        client = None
        _repo = repo
        if(redisConn != None):
            graphName = repo.RepositoryID + "-Relations"
            client = Client(repo.RepositoryID,conn=redisConn)
            graph = Graph(graphName,redisConn)
            
            try:
                client.drop_index()
                graph.delete()
            except:
                pass

            client.create_index((
                TextField("DocumentName",no_stem=True),
                TextField("Content",weight=1)),
                definition=IndexDefinition(prefix=['doc:'])
            )

            classes = []
            
            #indexing the document for Full Text Indexing
            #this section will index all files in the repository directory
            files = FileModel.objects.filter(RepositoryID = _repo.RepositoryID)
            for file in files:
                f = pathlib.Path(file.FilePath)
                if(file.IsDirectory == False and (f.suffix != '.pyc' and f.suffix != ".exe")):
                    print("read: {0}".format(file.FilePath))
                    content = open(file.FilePath,"r",errors='ignore').read()
                    client.redis.hset("doc:"+str(file.FileID),
                            # DocumentName = file.Filename,
                            # Content = content,
                            # replace=True
                        mapping={
                            'DocumentName' : file.Filename,
                            'Content' : content,
                        }
                    )


            #insert terms in redisearch
            # for doc in _repo.Documents:
            #     docID = uuid.uuid4()
            #     classes_in_doc = []
            #     content = open(doc.DocumentPath).read()
            #     for classModel in doc.Classes:
            #         classes_in_doc.append(classModel.Name)
            #         classes.append(classModel)
            #         for parent in classModel.Parents:
            #             classes_in_doc.append(parent.Name)
            #     # print(str(docID))
            #     # jsons.dumps(doc)
            #     strClassInDoc = " ".join(classes_in_doc)
            #     client.add_document("doc:"+str(docID),
            #             DocumentName = doc.DocumentName,
            #             Content = content,
            #             Classes = strClassInDoc,
            #             replace=True
            #         # mapping={
            #         #     'DocumentName' : doc.DocumentName,
            #         #     'Content' : content,
            #         #     'Classes' : strClassInDoc
            #         # }
            #     )

            #identifying classes in the whole repository
            for doc in _repo.Documents:
                for classModel in doc.Classes:
                    classes.append(classModel)
            
            #creating class relations
            #indexing meaningful terms in documents (class and functions)
            for doc in _repo.Documents:
                f = files.filter(FilePath = doc.DocumentPath).first()
                for classModel in doc.Classes:
                    baseClass = Node(label = "Class", properties = {
                        'ClassName': classModel.Name,
                        'Type' : classModel.Type,
                        'LineNo' : classModel.LineNo,
                        'ColOffset' : classModel.ColOffset,
                        'Namespace' : classModel.Namespace,
                        'FileID':str(f.FileID)
                    })
                    graph.add_node(baseClass)

                    for parent in classModel.Parents:
                        #check if parent is from this repository
                        x = list(filter(lambda y: y.Name == parent.Name and parent.Type != "attribute", classes))
                        if(len(x)>0):
                            pass
                            #using graph MERGE command to ensure that the node only exist once
                            #implemented later after all classes in this repository has been indexed as a node
                            # for parentCls in x:
                            #     queries = []
                            #     queries.append("""MERGE (parent:Class{{ClassName:"{0}",Type:"{1}",LineNo:{2},ColOffset:{3}}})""".format(parentCls.Name, parentCls.Type, parentCls.LineNo, parentCls.ColOffset))
                            #     queries.append("""MERGE (base:Class{{ClassName:"{0}",Type:"{1}",LineNo:{2},ColOffset:{3},FileID:"{4}"}})""".format(classModel.Name, classModel.Type, classModel.LineNo, classModel.ColOffset,str(f.FileID)))
                            #     queries.append("""MERGE (parent)-[r:parentOf]->(base)""")

                            #     graph.query(" ".join(queries))
                        
                            # for i in x:
                                # print(i.Name+" "+i.Type+" "+str(i.LineNo)+" "+str(i.ColOffset))
                                # parentClass = Node(label = "Class", properties = {
                                #     'ClassName': i.Name,
                                #     'Type' : i.Type,
                                #     'LineNo' : i.LineNo,
                                #     'ColOffset' : i.ColOffset
                                # })
                                # graph.merge()
                                # graph.add_node(parentClass)
                                # relation = Edge(parentClass,'parentOf',baseClass)
                                # graph.add_edge(relation)
                        else:
                            # print(parent.Name+" "+parent.Type)
                            # parentClass = Node(label = "Class", properties = {
                            #     'ClassName': parent.Name,
                            #     'Type' : parent.Type,
                            #     'LineNo' : '',
                            #     'ColOffset' : ''
                            # })
                            # graph.add_node(parentClass)
                            # relation = Edge(parentClass,'parentOf',baseClass)
                            # graph.add_edge(relation)
                            queries = []
                            queries.append("""MERGE (parent:Class{{ClassName:"{0}",Type:"{1}",LineNo:'',ColOffset:''}})""".format(parent.Name, parent.Type))
                            queries.append("""MERGE (base:Class{{ClassName:"{0}",Type:"{1}",LineNo:{2},ColOffset:{3},Namespace"{4}",FileID:"{5}"}})""".format(classModel.Name, classModel.Type, classModel.LineNo, classModel.ColOffset,classModel.Namespace,str(f.FileID)))
                            queries.append("""MERGE (parent)-[r:parentOf]->(base)""")

                            graph.query(" ".join(queries))

                    for funct in classModel.Functions:
                        functionNode = Node(label="Function", properties={
                            'Name':funct.Name,
                            'LineNo':funct.LineNo,
                            'ColOffset':funct.ColOffset
                        })
                        funcRelation = Edge(baseClass,'HasFunction',functionNode)
                        graph.add_node(functionNode)
                        graph.add_edge(funcRelation)

            graph.commit()

            #begin creating relations for nodes that already exist
            for doc in _repo.Documents:
                f = files.filter(FilePath = doc.DocumentPath).first()
                for classModel in doc.Classes:
                     for parent in classModel.Parents:
                        #check if parent is from this repository
                        x = list(filter(lambda y: y.Name == parent.Name and parent.Type != "attribute", classes))
                        if(len(x)>0):
                            #merge existing related node with this node if they have parent-child relationship
                            for parentCls in x:
                                queries = []
                                queries.append("""MATCH (parent:Class{{ClassName:"{0}",Type:"{1}",LineNo:{2},ColOffset:{3}}})""".format(parentCls.Name, parentCls.Type, parentCls.LineNo, parentCls.ColOffset))
                                queries.append("""MATCH (base:Class{{ClassName:"{0}",Type:"{1}",LineNo:{2},ColOffset:{3},FileID:"{4}"}})""".format(classModel.Name, classModel.Type, classModel.LineNo, classModel.ColOffset,str(f.FileID)))
                                queries.append("""MERGE (parent)-[r:parentOf]->(base)""")

                                graph.query(" ".join(queries))

            #creating autocompleter
            ac = AutoCompleter(repo.RepositoryID,conn=redisConn)
            for class in classes:
                ac.add_suggestions(class.Name)

            indexedRepository = IndexedRepositoryModel()
            indexedRepository.RediSearchClient = client
            indexedRepository.RedisGraphClient = graph
            return indexedRepository
    
    return None


