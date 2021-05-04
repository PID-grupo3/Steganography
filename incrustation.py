import numpy as np
import cv2
import itertools
from incrustationAuxiliar import * 

def incrustation(source,dest,message):
    cv2.imwrite(dest,DCT().incrustation(source,message))
    
    
filename = 'images/saved.png'    
photo="images/lenna.png"
dct_img = cv2.imread(photo, cv2.IMREAD_UNCHANGED)
message = "qwerty"
incrustation(dct_img, filename, message)