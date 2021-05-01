import numpy as np
import cv2
import itertools
from incrustationAuxiliar import * 

def incrustation(source,dest,message):
    cv2.imwrite(dest,DCT().incrustation(source,message))