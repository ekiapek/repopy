import jsons
from redisearch import Client,IndexDefinition,TextField,TagField
from redisgraph import Node, Edge, Graph, Path
from logic.RepositoryModel import ClassModel, IndexedRepositoryModel,RepositoryModel,ParentClassModel,DocumentModel
import uuid

def indexRepo(repo=None, redisConn=None):
    """
    do indexing on repository object with redisConn connection
    """
    if(repo != None):
        client = None
        _repo = repo
        if(redisConn != None):
            graphName = repo.RepositoryName + "-Relations"
            client = Client(repo.RepositoryName,conn=redisConn)
            graph = Graph(graphName,redisConn)

            client.create_index((
                TextField("DocumentName",no_stem=True),
                TextField("Content",weight=1),
                TextField("Classes",weight=2)), 
                definition=IndexDefinition(prefix=['doc:'])
            )

            classes = []
            
            #indexing the document
            for doc in _repo.Documents:
                docID = uuid.uuid4()
                classes_in_doc = []
                content = open(doc.DocumentPath).read()
                for classModel in doc.Classes:
                    classes_in_doc.append(classModel.Name)
                    classes.append(classModel)
                    for parent in classModel.Parents:
                        classes_in_doc.append(parent.Name)
                # print(str(docID))
                # jsons.dumps(doc)
                strClassInDoc = " ".join(classes_in_doc)
                client.add_document("doc:"+str(docID),
                        DocumentName = doc.DocumentName,
                        Content = content,
                        Classes = strClassInDoc,
                        replace=True
                    # mapping={
                    #     'DocumentName' : doc.DocumentName,
                    #     'Content' : content,
                    #     'Classes' : strClassInDoc
                    # }
                )
            
            #creating class relations
            for doc in _repo.Documents:
                for classModel in doc.Classes:
                    baseClass = Node(label = "Class", properties = {
                        'ClassName': classModel.Name,
                        'Type' : classModel.Type,
                        'LineNo' : classModel.LineNo,
                        'ColOffset' : classModel.ColOffset
                    })
                    graph.add_node(baseClass)

                    for parent in classModel.Parents:
                        x = list(filter(lambda y: y.Name == parent.Name and parent.type != "attribute", classes))
                        if(len(x)>0):
                            for i in x:
                                print(i.Name+" "+i.Type+" "+str(i.LineNo)+" "+str(i.ColOffset))
                                parentClass = Node(label = "Class", properties = {
                                    'ClassName': i.Name,
                                    'Type' : i.Type,
                                    'LineNo' : i.LineNo,
                                    'ColOffset' : i.ColOffset
                                })
                                graph.add_node(parentClass)
                                relation = Edge(parentClass,'parentOf',baseClass)
                                graph.add_edge(relation)
                        else:
                            print(parent.Name+" "+parent.Type)
                            parentClass = Node(label = "Class", properties = {
                                'ClassName': parent.Name,
                                'Type' : parent.Type,
                                'LineNo' : '',
                                'ColOffset' : ''
                            })
                            graph.add_node(parentClass)
                            relation = Edge(parentClass,'parentOf',baseClass)
                            graph.add_edge(relation)
            graph.commit()

            indexedRepository = IndexedRepositoryModel()
            indexedRepository.RediSearchClient = client
            indexedRepository.RedisGraphClient = graph
            return indexedRepository
    
    return None


