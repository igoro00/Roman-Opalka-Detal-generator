#created on 7.12.2019
#by Igor Ordecha

#image res = 15945 x 23031 @ 300dpi and original psyhical size
#number of lines = 471
#48px per row gives 22608px
#and to keep proportions as similar as possible width = 15652px
#that means 15652x22608 @ 11.5940px/mm and 135.001x194.997cm in psychical form

from PIL import Image, ImageDraw, ImageFont
import textwrap
from alive_progress import alive_bar
import time

def textWidth(string, cacheTable):
	output = 0
	for char in string:
		output += cacheTable[char]
	return output
def IntelliDraw(text,containerWidth, cacheTable):
    #todo: add one char at a time to line string and check if textsize fits containerWidth
    #if it overflows take that char back, break the innerloop and put it in the next line string
    #and again and again
    #until input it empty
    #then return all lines
    lines = []
    finished = False
    line = 0
    with alive_bar(len(text)) as bar:
        while not finished:
            newline = ""
            innerFinished = False
            while not innerFinished:
                if (textWidth(newline+text[:1], cacheTable)<= (containerWidth+10)) and len(text)>=1:
                    newline+=text[:1]
                    text = text[1:]
                    bar(text="1x speed", incr=1)
                else:
                    innerFinished = True
            if len(newline) > 0:
                lines.append(newline)
                line = line + 1
            else:
                finished = True
        return(lines)

def createCacheTable(drawer, font, charsToCache):
	cacheTable = dict()
	for char in charsToCache:
		cacheTable[char]=drawer.textsize(char, font)[0]
	return cacheTable
		
height = 22608
width = 15652

string = ""
for i in range(35327):
    string += str(i+1)
    string += " "
print("\nCreated string")

#creating B/W image
img = Image.new('L', (width, height), color=0)
fnt = ImageFont.truetype('FatBoyVeryRoundItalic.ttf', 39)
d = ImageDraw.Draw(img)
print("Created image")

cacheTable=createCacheTable(d, fnt, set(string))
print("Created cache table")

print("Wrapping text...")
wrapped = IntelliDraw(string, width, cacheTable)

print("Printing lines...")
h = 0
with alive_bar(len(wrapped), force_tty=True) as bar:
    for i in wrapped:
        d.text((5, h), i, font=fnt, fill=255)
        h += 49
        bar()

print("Saving...")
img.save('test.png')
print("Saved")



