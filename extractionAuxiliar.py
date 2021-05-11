import cv2
import math
import numpy as np
import itertools

class DCT():    
    def __init__(self): # Constructor
        self.message = None
        self.bitMess = None
        self.oriCol = 0
        self.oriRow = 0
        self.numBits = 0   
    #decoding part :
    
    def decode_image(self,img):
        row,col = img.shape[:2]

        messSize = None
        messageBits = []
        buff = 0
        med = 128

        #split image into RGB channels
        bImg = img[:,:,0]
        gImg = img[:,:,1]
        rImg = img[:,:,2]
       
        bImg = np.float32(bImg)

        #break into 8x8 blocks
        imgBlocks = [(bImg[j:j+8, i:i+8]-med) for (j,i) in itertools.product(range(0,row,8), range(0,col,8))]
        
        #blocks run through quantization table
        dctBlocks = [(cv2.dct(img_Block)) for img_Block in imgBlocks]
        
        i=0
        #message extracted from LSB of DC coeff
        iafasa = 0
        for quantizedBlock in dctBlocks:
            
            #print(quantizedBlock[0][0])
            DC = quantizedBlock[0][0]
            print("Bloque sin cuantizado: " + str(quantizedBlock[0][0]))

            DC = np.int16(DC) & 1
    
            
            iafasa = iafasa+1
            if(iafasa == 64):
                break
            if DC == 1:
                buff+=(0 & 1) << (7-i)
            elif DC == 0:
                buff+=(1&1) << (7-i)
            i=1+i
            if i == 8:
                messageBits.append(chr(buff))
                buff = 0
                i =0       
                if messageBits[-1] == '*' and messSize is None:
                    try:
                        messSize = int(''.join(messageBits[:-1]))
                    except:
                        pass
            if len(messageBits) - len(str(messSize)) - 1 == messSize:
                
                return ''.join(messageBits)[len(str(messSize))+1:]
            
        print(messageBits)
        print(len(str(messSize)))
        print(messSize)  
        
        return ''

