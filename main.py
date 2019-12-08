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


def IntelliDraw(drawer,text,font,containerWidth):
    #todo: add one char at a time to line string and check if textsize fits containerWidth
    #if it overflows take that char back, break the innerloop and put it in the next line string
    #and again and again
    #until input it empty
    #then return all lines
    lines = [] # prepare a return argument
    finished = False
    line = 0
    while not finished:
        newline = ""
        innerFinished = False
        while not innerFinished:
            print('thistext: '+str(newline))
            if drawer.textsize(newline,font)[0] < containerWidth:
                newline.insert(0,thistext.pop(-1))
            else:
                innerFinished = True
        if len(newline) > 0:
            lines.append(newline)
            line = line + 1
        else:
            finished = True
    tmp = []        
    for i in lines:
        tmp.append( ' '.join(i) )
    lines = tmp
    (width,height) = drawer.textsize(lines[0],font)            
    return (lines,width,height)


height = 22608
width = 15652

string = ""
for i in range(35327):
    string += str(i+1)
    string += " "
print("\nCreated string")

#creating B/W image
img = Image.new('L', (width, height), color=0)
fnt = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', 69) #xd
d = ImageDraw.Draw(img)
print("Created image")

#wrapped = [string[:491]]
#string = string[491:]
#wrapped.extend(textwrap.wrap(string, width=490))
wrapped = IntelliDraw(d, string, fnt, width)
print("Wrapped string")


print("\nGenerating lines..")

h = 0
with alive_bar(len(wrapped), force_tty=True) as bar:
    for i in wrapped:
        d.text((0, h), i, font=fnt, fill=255)
        h += 66
        bar()

print("\nSaving...")
img.save('test.png')
print("Saved\n")



