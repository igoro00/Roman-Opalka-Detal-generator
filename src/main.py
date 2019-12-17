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
from time import time, sleep
from os import mkdir
import argparse
from multiprocessing import Process

#*configuration 
#*▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#$ Default config down below is the result of calculation 
#$ at the top of this file (line 8).    
#$ You can change these settings but expect program to produce
#$ images different than Roman Opałka's paintings
height = 22608 #heigt in pixels                 
width = 15652 #width in pixels                  
density = 11.594 #density in px/mm              
targetNum = 100000 #program generates images until there's this number in some photo
lastNum = 1 #number that is printed first
bg = 0 #starting color for first image
growth = 1 #by how many % canvas brightens itself. 
#^^^^^  0-255 in 100/growth iterations
nodes = 4
#*▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#*end of configuration

def export(image):
    '''
        Exports image using provided objects.
        It can be running on infinite number of cores as there's no logic here
    '''
    gen.printText(image[3], image[2], image[1], image[4], image[6])
    gen.save(image[0], "output/"+image[5]+".png")


if __name__ == "__main__":
    #*runtime init stuff that can't be in the config
    startTime = time()
    try:
        mkdir("output")#make output dir if its missing
    except FileExistsError:
        pass
    growth = 255.0/(100.0/growth) #translates % to increase in 0-255 range
    renders = []
    maxLines = 0


    for i in range(nodes):
        renders.append(Process())
        renders[-1].start()
        renders[-1].terminate()
    
    while lastNum <= targetNum:

        #init picture
        img, fnt, d = gen.initImg(width, height, bg)
        cacheTable=gen.cacheTable(d, fnt, " 1234567890\n")
        if maxLines == 0:
            maxLines = gen.getMaxLines(d, fnt, height)
        
        # generating string and filename
        filename = str(lastNum) + '-'    
        wrapped, lastNum= gen.wrap(width, maxLines, cacheTable, d, fnt, lastNum)
        filename += str(lastNum)

        colors = paint.getColors(wrapped, bg)

        bg+=int(growth)
        lastNum += 1
        image = [img, fnt, d, wrapped, colors, filename, cacheTable]

        #jesli jest wolne to zajmij je i spierdalaj
        #jak nie ma wolnego to czekaj aż bedzie 
        freeNode = False
        j = 1
        while not freeNode:
            for i in range(len(renders)):
                if not renders[i].is_alive():
                    freeNode = True
                    j = i
            if not freeNode:
                sleep(1)
        else:
            renders[j] = Process(target=export, args=(image,))        
            renders[j].start()
                    

        
    #wait for all remaining render nodes to finish their jobs
    #and then measure time
    for i in range(len(renders)):
        renders[i].join()    
    print("\n\nDONE IN %ds\n\n"%(time()-startTime))