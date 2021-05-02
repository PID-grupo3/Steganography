import numpy as np
import cv2
import random
import gif2numpy
import tkinter as tk
import PIL.Image, PIL.ImageTk
from matplotlib import pyplot as plt


def readImage(e1, e2):
    if e1.get():
        photo="images/"+e1.get()+".png"
        cv_img = cv2.cvtColor(cv2.imread(photo), cv2.COLOR_BGR2RGB)
        #cv2.imwrite('log_transformed.jpg', img)
        openNewWindow(cv_img)
    return imgToShow
    
    
def showImage(imgToShow):
    cv2.imshow("Original image",imgToShow)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def openNewWindow(imgToShow):
      
    # Toplevel object which will 
    # be treated as a new window
    root = tk.Toplevel()
    root.geometry("500x300")
    root.resizable(0, 0)

    height, width, no_channels = imgToShow.shape 
    # sets the title of the
    # Toplevel widget
  
    # sets the geometry of toplevel
    canvas = tk.Canvas(root, width = width, height = height)    
    canvas.pack()  
            
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imgToShow))

    canvas.create_image(0, 0, image=photo, anchor=tk.NW) 

    root.mainloop()
    
def otra(cv_img):
    window = tkinter.Tk()
    window.title("OpenCV and Tkinter")
    
    # Load an image using OpenCV
    
    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
    height, width, no_channels = cv_img.shape
    
    # Create a canvas that can fit the above image
    canvas = tkinter.Canvas(window, width = width, height = height)
    canvas.pack()
    
    # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))

    # Add a PhotoImage to the Canvas
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    
    # Run the window loop
    window.mainloop()