#! /usr/bin/python3
try:
    from PIL import Image as Im
except ImportError:
    import Image as Im

from os import remove,chdir,path,remove,getenv

from pytesseract.pytesseract import image_to_string

from UrlDown import GetFileName
from random import randint

import multiprocessing as MultiPro


ToDelete = []

def OcrCore(Image,UserLang=None):
    
    if UserLang == None:
        
        text = image_to_string(Im.open(Image))
        
        #print(text)
       
        return text
    else:

        text = image_to_string(Image,lang=UserLang).split(' ')
       
        return text


def HorizontalHalfOne(x):
    
    ImageFile = Im.open(x)
    width,height = ImageFile.size

    size = (0,height/2,width,height)
    new_image = ImageFile.crop(size)

    FileName = f"upper_{x}"
    new_image.save(FileName)
    
    ToDelete.append(FileName)
    
    return FileName
    
def HorizontalHalfTwo(x):
    ImageFile = Im.open(x)
    width,height = ImageFile.size
    size = (0,0,width,height/2)

    NewImage = ImageFile.crop(size)
    FileName = f"lower_{x}"
    NewImage.save(FileName)
    
    ToDelete.append(FileName)
    
    return FileName

def DecideSplit(x):

    Image = Im.open(x)
    Height = Image.size[1]

    #My Goal here is that if the height is less than 100 pixel
    #Then you dont need to split the image into Half just read it

    if Height < 100:
        # Then no need to split just return the opened ImageFile
    
        return x,"None"
    
    else:
        #Just usually split the image and return both the halves
        
        (UpperHalf,LowerHalf) = HorizontalHalfOne(x),HorizontalHalfTwo(x)
        
        return UpperHalf,LowerHalf

def EnlargeImage(x,factor=2):
    
    
    Image = Im.open(x)
    Height = Image.size[1]
    if Height > 600:
        return x
        
    else:    
        NewSize = tuple(factor*x for x in Image.size)
        # This means for every pixel in given x image file,
        # Copy it by the scale of factor times x or enlarge by factor*x
    
        NewImage = Image.resize(NewSize, Im.ANTIALIAS).convert("L")
        FileName = f"enlarged_{x}"
        NewImage.save(FileName)
        
        ToDelete.append(FileName)
    
        return FileName

def remove_files(x:list):
    for i in x:
        remove(i)


def PrintText(Image):
    Text = OcrCore(Image)
    print(Text)


if __name__ == "__main__":
    
    File = #Your FileName
    #Most likely you won't like hardcoding images files then instead you
    # could use sys module and take command line arguments
    
    FileName = GetFileName(File)
    chdir(path.dirname(File))
    
    enlarged = EnlargeImage(FileName,2)
    split1,split2 = DecideSplit(enlarged)
    
    if split2 == "None":
        Text = OcrCore(split1)
    else:
        ImageList = [split1,split2]
        
        #Creating a pool for our processes
        #Multiprocessing
        with MultiPro.Pool() as pool:
            pool.map(PrintText,ImageList)
        
        #Ending part
        #All these files which were created now needed to be delted
        remove_files(ToDelete)
        
        
