#created on 7.12.2019
#by Igor Ordecha

#image dimensions = 135x195cm
#image res = 15945 x 23031 @ 300dpi with original psyhical size
#number of lines = 471
#48px per row gives 22608px
#and to keep proportions as similar as possible width = 15652px
#that means 15652x22608 @ 11.5940px/mm and 135.001x194.997cm in psychical form

import generator as gen
import paint
from time import time
from os import mkdir


#*configuration 
#$ Default config down below is the result of calculation 
#$ at the top of this file (line 8).
#$ You can change these settings but expect program to produce
#$ images different than Roman Opałka's paintings
height = 22608 #heigt in pixels
width = 15652 #width in pixels
density = 11.594 #density in px/mm
targetNum = 7777777 #program generates images until this number appears in some image
lastNum = 1 #number that is printed first
bg = 0 #starting color for first image
growth = 1 #by how many % canvas brightens itself. 
#^^^^^  0-255 in 100/growth iterations 



#* actual program
startTime = time()
growth = 255.0/(100.0/growth) #translates % to increase in 0-255 range  
imageIndex = 1
while lastNum < targetNum:
    print("\nPICTURE #%d"%imageIndex)

    #init picture
    img, fnt, d = gen.initImg(width, height, bg)
    cacheTable=gen.cacheTable(d, fnt, " 1234567890\n")
    maxLines = gen.getMaxLines(d, fnt, height)

    # generating string and filename
    filename = str(lastNum) + '-'    
    wrapped, lastNum= gen.wrap(width, maxLines, cacheTable, d, fnt, lastNum)
    filename += str(lastNum)
    lastNum+=1 #without this, image start with the same number as previous image ends with     

    # export image
    colors = paint.getColors(wrapped, bg)
    gen.printText(wrapped, d, fnt, colors, cacheTable)
    try:
        mkdir("output")#make output dir if its missing
    except FileExistsError:
        pass
    gen.save(img, "output/"+filename+".png")
    
    # make canvas brigther by growth%
    bg += int(growth)

    imageIndex += 1
print("\n\n\n\nDONE IN %ds"%(time()-startTime))
  