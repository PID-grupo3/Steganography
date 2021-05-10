import cv2
import math
import numpy as np
import itertools

quant2 = np.array([[16,11,10,16,24,40,51,61],      # QUANTIZATION TABLE
                    [12,12,14,19,26,58,60,55],    # required for DCT
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

quant = np.array([[8, 8 ,8, 9, 1 ,1 ,1, 1],
                    [8, 8 ,9 ,1 ,1, 1 ,1 ,14],
                    [8 ,9 ,1 ,1 ,1 ,1 ,14 ,15],
                    [9 ,1 ,1 ,1 ,1 ,14 ,15 ,16],
                    [1 ,1 ,1 ,1 ,14 ,15 ,16 ,18],
                    [1 ,1 ,1 ,14 ,15 ,16 ,18 ,20],
                    [1 ,1 ,14 ,15 ,16 ,18 ,20 ,22],
                    [1 ,14 ,15 ,16 ,18 ,20 ,22 ,23]])

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
        bImg,gImg,rImg = cv2.split(img)
       
        bImg = np.float32(bImg)
    
        #break into 8x8 blocks
        imgBlocks = [(bImg[j:j+8, i:i+8]-med) for (j,i) in itertools.product(range(0,row,8), range(0,col,8))]
        
        #blocks run through quantization table
        dctBlocks = [(cv2.dct(img_Block)) for img_Block in imgBlocks]
        
        i=0
        #message extracted from LSB of DC coeff
        iafasa = 0
        for quantizedBlock in dctBlocks:
            
            DC = quantizedBlock[0][0]
            DC = np.uint8(DC)
            DC = np.unpackbits(DC)
            
            #iafasa = iafasa+1
            #if(iafasa == 64):
            #    break
            if DC[7] == 1:
                buff+=(0 & 1) << (7-i)
            elif DC[7] == 0:
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

