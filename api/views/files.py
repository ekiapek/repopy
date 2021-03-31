from django.http import FileResponse

def getFile(request):
    file = open("C:\\Users\\ASUS\\Documents\\repopy\\logic\\Burger.py","rb")
    return FileResponse(file)