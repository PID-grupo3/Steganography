import cv2
from extractionAuxiliar import decode_image
import matplotlib.pyplot as plt
def extraction(imagen):
    mensaje,heatMap,imgBlock,EncriptedImg = decode_image(imagen)
    return mensaje,heatMap,imgBlock,EncriptedImg

    

photo="images/saved.png"
dct_img = cv2.imread(photo, -1)
mensaje,heatMap,imgBlock,EncriptedImg = extraction(dct_img)
plt.show()