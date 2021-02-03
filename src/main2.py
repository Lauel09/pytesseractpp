#! /usr/bin/python3
try:
    from PIL import Image as Im
except ImportError:
    import Image as Im

from os import remove,chdir,path,remove,getcwd
from pkgutil import read_code

from pytesseract.pytesseract import image_to_string

from UrlDown import GetFileName
from threading import Thread

from sys import argv

class image_object:
    
    def __init__(self,file_path) -> None:
        self.file_path = file_path
        self.file_name = GetFileName(file_path)
        self.ToDelete = []
    
    def chng_dir(self):
        if self.file_path == path.dirname(self.file_path):
            pass
        else:
            chdir(path.dirname(self.file_path))

    def upper_half(self):

        ImageFile = Im.open(self.file_name)
        width, height = ImageFile.size
        #This is for a split in half horizontally
        size = (0, height/2, width, height)
        new_image = ImageFile.crop(size)

        FileName = f"upper_{self.file_name}"
        new_image.save(FileName)

        self.ToDelete.append(FileName)

        return FileName

    def DecideSplit(self,x):

        Image = Im.open(x)
        Height = Image.size[1]

    #My Goal here is that if the height is less than 100 pixel
    #Then you dont need to split the image into Half just read it
        if Height < 200:
            # Then no need to split just return the opened ImageFile
            return x, "NONE"
        else:
            #Just usually split the image and return both the halves
            (UpperHalf, LowerHalf) = self.upper_half(), self.lower_half()

            return UpperHalf, LowerHalf


    def lower_half(self):
        ImageFile = Im.open(self.file_name)
        
        width, height = ImageFile.size
        size = (0, 0, width, height/2)

        NewImage = ImageFile.crop(size)
        FileName = f"lower_{self.file_name}"
        NewImage.save(FileName)

        self.ToDelete.append(FileName)

        return FileName

    def OcrCore(Image,UserLang=None):
    
        if UserLang == None:
        
            text = image_to_string(Im.open(Image))
            #print(text)
            return text
        else:
            text = image_to_string(Image,lang=UserLang).split(' ')
       
            return text


    def EnlargeImage(self,factor=2):
        self.chng_dir()
        Image = Im.open(self.file_name)
        Height = Image.size[1]
        if Height > 600:
            return self.file_name

        else:
            NewSize = tuple(factor*x for x in Image.size)
            # This means for every pixel in given x image file,
            # Copy it by the scale of factor times x or enlarge by factor*x

            NewImage = Image.resize(NewSize, Im.ANTIALIAS).convert("L")
            FileName = f"enlarged_{self.file_name}"
            NewImage.save(FileName)

            self.ToDelete.append(FileName)

            return FileName
    

    def remove_files(x:list):
        for i in x:
            remove(i)

def PrintText(Image):
    Text = read_image(Image)
    print(Text)

def read_image(Image, UserLang=None):
    if UserLang == None:

        text = image_to_string(Im.open(Image))
    #print(text)
        return text
    else:
        text = image_to_string(Image, lang=UserLang).split(' ')
        return text
    
if __name__ == "__main__":
    
    if len(argv) > 1:
        
        file = image_object(argv[1])

        enlarged = file.EnlargeImage(2)
        split1, split2 = file.DecideSplit(enlarged)

        if split2 == "None":
            #In conditions like this there is no need for multithreading
            #Image is already so small, introducing threading would bring 
            #unnecessary overhead
            
            Text = file.read_image(split1)
        else:
            #We need threading, to make stuffs fast
            # Give one task to extra thread whle other one to main thread
            #No need to to create two different threads
            
            ThreadOne = Thread(target=PrintText, args=(split1,))
             PrintText(split2)
                
            ThreadOne.start()
            ThreadOne.join()
           
            file.remove_files()
    else:
        print("Not enough args")
        exit(1)
    
    
        
        
