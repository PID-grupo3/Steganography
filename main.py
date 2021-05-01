import numpy as np
import cv2
import random
import gif2numpy
from matplotlib import pyplot as plt
 
 
 
def main():
    
    print() #Salto de línea
    print("##############################################################################################")
    print("############## BIENVENIDO AL PROGRAMA PARA INCRUSTAR INFORMACIÓN EN UNA IMAGEN ###############")
    print("##############################################################################################")
    print() #Salto de línea
    print("INTRODUZCA EL NOMBRE DE LA IMAGEN:")
    userPhoto=input()
    photo="images/"+userPhoto+".png"
    img = cv2.imread(photo, -1)
    imgToShow = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    plt.title("Imagen original")
    cv2.imwrite('log_transformed.jpg', imgToShow)
    
    # Incrustacion o extraccion
    
    
    
    
main()