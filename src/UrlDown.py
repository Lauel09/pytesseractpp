from os import path,chdir,remove
import requests as req
from random import randint
from pathlib import Path
from PIL import Image as Im
from shutil import copy2

def CheckFileExt(x:str):

    File = Im.open(x)
    return File.format.lower()

#Just a helper method
def DownMultipleImages(x:list,FolderPath:str):
    try:
        if path.exists(FolderPath):
            chdir(FolderPath)
        else:
            Path(FolderPath).mkdir(parents = True,exist_ok = False)
            chdir(FolderPath)
    except:
        False

    for i in x:
        File = req.get(i,stream =  True)
        FileExt = CheckFileExt(i)
        if FileExt == "Unknown":
            FileExt = ''
        if File.status_code == 200:# This means we have got some response body

            with open(f"random{randint(1,100000000)}.{FileExt}","wb") as file:
                file.write(File.content)
                
                #Writing to the file as binary
        else:
            print("Got no response body!")
    return True

def OpenReadUrl(x):
    with open(x,'r') as File:
        data = File.read().split('\n')
        return data
    
def SaveFileWithFormat(x):

    NewFile = f"{x}.{CheckFileExt(x)}"

    with open(NewFile,'w') as File:
        pass
    copy2(x,NewFile)
    #After this all delete the previous one
    remove(x)

"""
Instead of this function you can do something like:-
def ReturnBi(x):
    Image = Im.open(x)
    NewImage = Image.convert("L")
"""
#What do with the file would be your choice    
def SaveFileToBi(x):
    FolderPath = path.dirname(x)
    chdir(FolderPath)

    dun = x.split('/')

    FileName = dun[len(dun)-1]
    Thresh = 200

    ImageFile = Im.open(FileName)

    # Currently using a lambda function
    # If the given x > Thresh(200) then the return value is 255 else it is 0

    def Fn(x): return 255 if x > Thresh else 0

    file = ImageFile.convert("L").point(Fn, mode='1')

    file.save(f"bi_{FileName}")
    #Deleting the copy would be in your hand


def ConvertFileToBi(x):
    ImageFile = Im.open(x)

    Thresh = 200
    def Fn(x): return 255 if x > Thresh else 0

    File = ImageFile.convert("L").point(Fn, mode='1')
    FileName = f"bi_{randint(0,10)}_{x}"
    File.save(FileName)

    return FileName

def GetFileName(x):
    return x.split('/')[len(x.split('/'))-1]