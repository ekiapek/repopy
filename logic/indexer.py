from redisearch import Client,IndexDefinition,TextField,TagField
from redisgraph import Node, Edge, Graph, Path
from .RepositoryModel import ClassModel, IndexedRepositoryModel,RepositoryModel,ParentClassModel,DocumentModel
import uuid

def indexer(repo=None, redisConn=None):
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

            client.create_index(
                TextField("DocumentName",no_stem=True),
                TextField("Content"),
                TagField("Classes",weight=2)
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
                
                strClassInDoc = ','.join(classes_in_doc)
                client.redis.hset(str(docID),
                    mapping={
                        'DocumentName' : doc.DocumentName,
                        'Content' : content,
                        'Classes' : strClassInDoc
                    }
                )
            
            #creating class relations
            for doc in _repo.Documents:
                for classModel in doc.Classes:
                    baseClass = Node(label = classModel.Name, properties = {
                        'ClassName': classModel.Name,
                        'Type' : classModel.Type,
                        'LineNo' : classModel.LineNo,
                        'ColOffset' : classModel.ColOffset
                    })
                    graph.add_node(baseClass)

                    for parent in classModel.Parents:
                        x = filter(lambda y: y.Name == parent.Name, classes)
                        if(len(x)>0):
                            for i in x:
                                parentClass = Node(label = i.Name, properties = {
                                    'ClassName': i.Name,
                                    'Type' : i.Type,
                                    'LineNo' : i.LineNo,
                                    'ColOffset' : i.ColOffset
                                })
                                graph.add_node(parentClass)
                                relation = Edge(parentClass,'parent-of',baseClass)
                                graph.add_edge(relation)
                        else:
                            parentClass = Node(label = parent.Name, properties = {
                                'ClassName': parent.Name,
                                'Type' : parent.Type,
                                'LineNo' : '',
                                'ColOffset' : ''
                            })
                            graph.add_node(parentClass)
                            relation = Edge(parentClass,'parent-of',baseClass)
                            graph.add_edge(relation)
            graph.commit()

            indexedRepository = IndexedRepositoryModel()
            indexedRepository.RediSearchClient = client
            indexedRepository.RedisGraphClient = graph
            return indexedRepository
    
    return None


