import numpy as np
import cv2
import random
import gif2numpy
import tkinter as tk
import PIL.Image, PIL.ImageTk
from matplotlib import pyplot as plt
from incrustation import *
from extraction import *


def readImage(e1, e2):
    if e1.get():
        photo="images/"+e1.get()+".png"
        cv_img = cv2.imread(photo, 1)
        imgToShow = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        #cv2.imwrite('log_transformed.jpg', img)
        openNewWindow(imgToShow, e2.get())
        
def extraction(image):
 
    photo="images/"+image+".jpg"
    cv_img = cv2.imread(photo, 1)
    #imgToShow = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    #cv2.imwrite('log_transformed.jpg', img)
    openWindowExtraction(cv_img)
    
    
    
def showImage(imgToShow):
    cv2.imshow("Original image",imgToShow)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def openNewWindow(imgToShow, message):
 
    #def get_coordinates(event):
    #    canvas.itemconfigure(tag, text='({x}, {y})'.format(x=event.x, y=event.y)) 

    root = tk.Toplevel()
    
    canvas = tk.Canvas(root, height=250, width=400)
    
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imgToShow))
    photo = photo._PhotoImage__photo.subsample(2)
    
    canvas.create_image(0, 0, anchor="nw", image=photo)
    root.resizable(width=False, height=False)
    
    widget = tk.Label(canvas, text='Message to encript: ' + message)
    widget.pack()
    
    canvas.create_window(70, 206, window=widget)  
    
    #canvas.bind('<Motion>', get_coordinates)
    #canvas.bind('<Enter>', get_coordinates)  # handle <Alt>+<Tab> switches between windows
    #tag = canvas.create_text(10, 10, text='', anchor='nw') 
    canvas.pack()
    
    filename = 'savedImage.jpg'
    
    quitButton = tk.Button(root, text='Return to main', command=root.destroy)
    quitButton.place(x=200, y=10)   
    
    stepButton = tk.Button(root, text='Step by step calculation', command= lambda: incrustationStep(imgToShow,filename, message))
    stepButton.place(x=200, y=50)   
    
    directButton = tk.Button(root, text='Direct calculation', command=lambda: incrustation(imgToShow,filename, message))
    directButton.place(x=200, y=90)   
    
    

    root.mainloop()
    
def openWindowExtraction(imgToShow):
    
    # Create basic Tkinter structure
    #def get_coordinates(event):
    #    canvas.itemconfigure(tag, text='({x}, {y})'.format(x=event.x, y=event.y)) 

    root = tk.Toplevel()
    
    canvas = tk.Canvas(root, height=250, width=400)
    
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imgToShow))
    photo = photo._PhotoImage__photo.subsample(2)
    
    canvas.create_image(0, 0, anchor="nw", image=photo)
    root.resizable(width=False, height=False)
    
    #canvas.bind('<Motion>', get_coordinates)
    #canvas.bind('<Enter>', get_coordinates)  # handle <Alt>+<Tab> switches between windows
    #tag = canvas.create_text(10, 10, text='', anchor='nw') 
    canvas.pack()
    
    quitButton = tk.Button(root, text='Return to main', command=root.destroy)
    quitButton.place(x=200, y=10)   
    
    stepButton = tk.Button(root, text='Step by step calculation', command= lambda: incrustationStep(imgToShow,filename, message))
    stepButton.place(x=200, y=50)   
    
    directButton = tk.Button(root, text='Direct calculation', command=lambda: extraction(imgToShow))
    directButton.place(x=200, y=90)   
    
    root.mainloop()