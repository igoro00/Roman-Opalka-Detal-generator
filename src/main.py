#created on 7.12.2019
#by Igor Ordecha

#image res = 15945 x 23031 @ 300dpi and original psyhical size
#number of lines = 471
#48px per row gives 22608px
#and to keep proportions as similar as possible width = 15652px
#that means 15652x22608 @ 11.5940px/mm and 135.001x194.997cm in psychical form

import utils
import paint

height = 22608
width = 15652
lastNum = 1
bg = 0

img, fnt, d = utils.initImg(width, height, bg)          # *
cacheTable=utils.cacheTable(d, fnt, " 1234567890\n")    # *init the picture
maxLines = utils.getMaxLines(d, fnt, height)            # *

filename = str(lastNum) + '-'    
wrapped, lastNum= utils.wrap(width, maxLines, cacheTable, d, fnt, lastNum)
filename += str(lastNum)        # *generating string and filename

colors = paint.getColors(wrapped, bg)
utils.printText(wrapped, d, fnt, colors, cacheTable)    #* export image
utils.save(img, filename+".png")    #*
