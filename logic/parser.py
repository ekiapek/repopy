import astroid
import glob
import sys
import traceback

def parseCode(base_dir):
    # root_dir needs a trailing slash (i.e. /root/dir/)
    for filename in glob.iglob(base_dir + '**/*.py', recursive=True):
        try:
            file = open(filename).read()
            code = astroid.parse(file)
            for node in code.body:
                if(isinstance(node,astroid.ClassDef)):
                    print("\n"+filename)
                    if(len(node.bases)>0):
                        print(node.name+" Parent: ")
                        for base in node.bases:
                            if(isinstance(base,astroid.Attribute)):
                                print(base.attrname)
                            else:
                                print(base.name)
                    else:
                        print(node.name)
        except Exception as e:
            print("ERROR:")
            print(e)
            traceback.print_tb(e.__traceback__)
        # pass

parseCode('C:\\Users\\ASUS\\Documents\\repopy\\')