from PIL import Image, ImageDraw, ImageFont
from alive_progress import alive_bar
def initImg(width, height, font='FatBoyVeryRoundItalic.ttf', size = 41):
    #creating B/W image
    img = Image.new('L', (width, height), color=0)
    fnt = ImageFont.truetype('FatBoyVeryRoundItalic.ttf', 41)
    d = ImageDraw.Draw(img)
    print("Created image")
    return img, fnt, d

def lastLine(string):
    i = string.rfind("\n") + 1
    return string[i:]

def textWidth(string, cacheTable):
	output = 0
	for char in string:
            output += cacheTable[char]
	return output

def wrap(width, maxLines, cacheTable, drawer, font, count):
    print("Creating text...")
    string = ""
    newNum = ""
    lines = 0
    finished = False
    with alive_bar() as bar:
        while not finished: 
            innerFinished = False
            while not innerFinished:
                if len(newNum)>0:  
                    if textWidth(lastLine(string)+newNum[:1], cacheTable)<= width:
                        string+=newNum[:1]
                        newNum = newNum[1:]
                        bar(text = "dict", incr=1)
                    elif drawer.textsize(lastLine(string)+newNum[:1], font)[0] <= width:
                        #if it reaches the end of the line fast way, then we need
                        #to check for missing ending with trusted and slow way
                        string+=newNum[:1]
                        newNum = newNum[1:]
                        bar(text="non-dict", incr=1)
                    else:
                        string += "\n"
                        lines += 1
                        innerFinished = True
                else:
                    newNum += str(count) + " "
                    count += 1
            if lines >= maxLines:
                finished = True
        return(string)

def cacheTable(drawer, font, charsToCache):
    cacheTable = dict()
    for char in charsToCache:
        cacheTable[char]=drawer.textsize(char, font)[0]
    print("Created cache table")
    return cacheTable
		
def string(maxChars, start):
    string = ""
    while len(string)<maxChars:
        string += str(start) + " "
        start += 1
    print("Created string\n\n\n")
    return string, start

def getMaxLines(drawer, font, height):
    i = 0
    while drawer.textsize("0\n"*i, font)[1]<height:
        i += 1
    print("Calculated max. number of lines")
    return i
def printText(string, d, fnt):
    d.text((5, 0), string, font=fnt, fill=255)
    print("Printed text...")

def save(img, filename):
    print("Saving...")
    img.save(filename)
    print("Saved")