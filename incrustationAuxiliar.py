import numpy as np
import cv2
import itertools
import math

class DCT():    
    def __init__(self): # Constructor
        self.message = None
        self.bitMess = None
        self.oriCol = 0
        self.oriRow = 0
        self.numBits = 0   
    #encoding part : 
    def incrustation(self,img,secret):
        
        self.message = str(len(secret))+'*'+secret
        self.bitMess = self.toBits()

        #get size of image in pixels
        row,col = img.shape[:2]
        self.oriRow, self.oriCol = row, col  

        if((col/8)*(row/8)<len(secret)):
            print("Error: Message too large to encode in image")
            return      
        
        #cv2.imshow('g',gray)
        #cv2.imshow('i', img2)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #make divisible by 8x8
        if row%8 != 0 or col%8 != 0:
            img = self.addPadd(img, row, col)
        
        row,col = img.shape[:2]

        #split image into RGB channels
        
        bImg = img[:,:,0]
        gImg = img[:,:,1]
        rImg = img[:,:,2]
        
        sImg = self.incrustationCore(bImg, row,col)
       
        possibleFinal = cv2.merge((sImg, gImg, rImg))
        
        diferenciaTotal = possibleFinal - img
        errorNumericoTotal = np.mean(diferenciaTotal**2) 
        errorNumericoTotal
        
        cv2.imwrite('images/error.png' ,diferenciaTotal) 
        
        print(errorNumericoTotal)
        
        return possibleFinal

    def chunks(self, l, n):
        m = int(n)
        for i in range(0, len(l), m):
            yield l[i:i + m]
            
    def addPadd(self,img, row, col):
        img = cv2.resize(img,(col+(8-col%8),row+(8-row%8)))    
        return img
    
    def toBits(self):
        bits = []
        for char in self.message:
            binval = bin(ord(char))[2:].rjust(8,'0')
            bits.append(binval)  
        self.numBits = bin(len(bits))[2:].rjust(8,'0')
        return bits
    
    def addBits(self, bit, number):
        andMask = np.int16(0b1111111111111110)
        
        # Bit es int16
        # Number es int16
                
        return (number & andMask) | bit
    
    
    def incrustationCore(self, bImg, row,col):
        
        med = 128
        
        bImg = np.float32(bImg)
        
        print(bImg[0])
    
        #break into 8x8 blocks
        imgBlocks = [(bImg[i:i+8, j:j+8]-med) for (i,j) in itertools.product(range(0,row,8), range(0,col,8))]
        
        #Blocks are run through DCT function
        dctBlocks = [(cv2.dct(img_Block)) for img_Block in imgBlocks]
        
        #set LSB in DCT value corresponding bit of message
        messIndex = 0
        letterIndex = 0
        for quantizedBlock in dctBlocks:
  
            #find LSB in DC coeff and replace with message bit
            DC = quantizedBlock[0][0]
            DC = np.int16(DC)     
    
            bit = self.bitMess[messIndex][letterIndex]
            
            if bit == '1':
                bit = 1
            else:
                bit = 0
            
            quantizedBlock[0][0] = self.addBits(bit, DC)
            print("Bloque cuantizado: " + str(quantizedBlock[0][0]))
    
            letterIndex = letterIndex+1
            if letterIndex == 8:
                letterIndex = 0
                messIndex = messIndex + 1
                if messIndex == len(self.message):
                    break

        #blocks run inversely through quantization table
        #sImgBlocks = [quantizedBlock*quant+med for quantizedBlock in quantizedDCT]
        
        #blocks run through inverse DCT
        
        sImgBlocks = [cv2.idct(B)+med for B in dctBlocks]
        
        #print(sImgBlocks[0][0])
        
        #puts the new image back together
        sImg=[]
        # LA RECONSTRUCCION ESTA MAL
        for chunkRowBlocks in self.chunks(sImgBlocks, col/8):
            for rowBlockNum in range(8):
                for block in chunkRowBlocks:
                    sImg.extend((block[rowBlockNum]))
        #print(sImg)         
        sImg = np.array(sImg).reshape(row, col)
        
        #converted from type float32
        sImg = np.ceil(sImg)
        sImg = np.uint8(sImg)
        
        #print(sImg[0])

        return sImg
    
    
    
    def incrustationCoreNoImage(self, bImg, row,col):
        
        bImg = np.float32(bImg)
        #print(bImg[0:8,0:8])
        
        #break into 8x8 blocks
        imgBlocks = [np.round(bImg[j:j+8, i:i+8]) for (j,i) in itertools.product(range(0,row,8), range(0,col,8))]
        #print(imgBlocks[1][0])
        #Blocks are run through DCT function
        dctBlocks = [np.round(cv2.dct(img_Block)) for img_Block in imgBlocks]

        #blocks then run through quantization table
        quantizedDCT = [np.round(dct_Block/quant) for dct_Block in dctBlocks]

        #blocks run inversely through quantization table
        #sImgBlocks = [quantizedBlock *quant+128 for quantizedBlock in quantizedDCT]
        
        #blocks run through inverse DCT
        sImgBlocks = [cv2.idct(G)+128 for G in quantizedDCT]
        
        #puts the new image back together
        sImg=[]
        for chunkRowBlocks in self.chunks(sImgBlocks, col/8):
            for rowBlockNum in range(8):
                for block in chunkRowBlocks:
                    sImg.extend(block[rowBlockNum])
        sImg = np.array(sImg).reshape(row, col)
        #converted from type float32
        sImg = np.uint8(sImg)
        
        return sImg