import numpy as np
import cv2
import random
import gif2numpy
from matplotlib import pyplot as plt
from mainAuxiliar import *
import tkinter as tk
from tkinter import ttk
 
 
def main():
    
    root = tk.Tk()
    
    def enableDissable(*args):
        y = stringvar1.get()
        z = stringvar2.get()
        if y and z:
            button.config(state='normal')
        else:
            button.config(state='disabled')
            
    def enableDissableExtraction(*args):
        y = stringvar1.get()
        z = stringvar2.get()
        if y and not(y and z):
            button2.config(state='normal')
        else:
            button2.config(state='disabled')
   
    
    root.geometry("500x300")
    root.resizable(0, 0)
    
    label1 = tk.Label(root, text="Name of the image")
    label1.grid(row=0)
    
    label2 = tk.Label(root, text="Text to encript")
    label2.grid(row=1)
    
    stringvar1 = tk.StringVar(root)
    stringvar2 = tk.StringVar(root)

    stringvar1.trace("w", enableDissable)
    stringvar2.trace("w", enableDissable)
    stringvar1.trace("w", enableDissableExtraction)
    stringvar2.trace("w", enableDissableExtraction)
 
    e1 = tk.Entry(root, textvariable=stringvar1)
    e2 = tk.Entry(root, textvariable=stringvar2)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    
    quitButton = tk.Button(root, text='Quit', command=root.quit)
    quitButton.grid(row=3, column=0, sticky=tk.W, pady=4)      
    
    button = tk.Button(root, text='Incrustation', command= lambda: readImage(e1, e2))
    button.grid(row=3, column=1, sticky=tk.W, pady=4)
    
    button2 = tk.Button(root, text='Extraction', command= lambda: extractionAux(e1.get()))
    button2.grid(row=6, column=1, sticky=tk.W, pady=4)
    
    enableDissable()
    enableDissableExtraction()
    
    root.mainloop()
    
main()