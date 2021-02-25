from redbaron import RedBaron
import glob

def parseCode(base_dir):
    # root_dir needs a trailing slash (i.e. /root/dir/)
    for filename in glob.iglob(base_dir + '**/*.py', recursive=True):
        with open(filename) as source_code:
            red = RedBaron(source_code.read())
            a = red.find_all('ClassNode')
            if(len(a)>0):
                print("\n"+filename)
            for x in a:
                if(len(x.inherit_from)>0):                    
                    print("Class "+x.name+" Parent:")
                    for i in x.inherit_from:
                        print(i.value)
                else:
                    print("Class "+x.name)
                    pass
    # pass

parseCode('C:\\Users\\ASUS\\Documents\\repopy\\')