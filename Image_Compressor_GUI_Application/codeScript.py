#Resizes an image and keeps aspect ratio. Set mywidth to the desired with in pixels.

import PIL
from PIL import Image
import os

mywidth = 3120
source_dir = 'C:/Users/91911/Desktop/Application/photo'
dest_dir = 'C:/Users/91911/Desktop/Application/photo1'

def resize_image(old_pic, new_pic, mywidth):
    img = Image.open(old_pic)  ##r'C:\Users\91911\Desktop\Application\IMG_20180415_143830.jpg'
    wpercent = (mywidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
    img.save(new_pic) ## C:\Users\91911\Desktop\Application\resize_image1.jpg

def entire_directory(source_dir, dest_dir,mywidth):
    files = os.listdir(source_dir)

    i=0
    for file in files:
        i += 1
        old_pic = source_dir + '/' + file
        new_pic = dest_dir + '/' +file       
        resize_image(old_pic, new_pic,mywidth)
        print(i,"done")

entire_directory(source_dir,dest_dir,mywidth)

