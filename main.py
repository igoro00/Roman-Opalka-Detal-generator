#created on 7.12.2019
#by Igor Ordecha

#image res = 15945 x 23031 @ 300dpi and original psyhical size
#number of lines = 471
#48px per row gives 22608px
#and to keep proportions as similar as possible width = 15652px
#that means 15652x22608 @ 11.5940px/mm and 135.001x194.997cm in psychical form

import utils

height = 22608
width = 15652
lastNum = 1
filename ="1"


img, fnt, d = utils.initImg(width, height)
cacheTable=utils.cacheTable(d, fnt, " 1234567890\n")
maxLines = utils.getMaxLines(d, fnt, height)
utils.printText(utils.wrap(width, maxLines, cacheTable, d, fnt, lastNum), d, fnt)
utils.save(img, filename+".png")

