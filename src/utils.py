from PIL import Image, ImageDraw, ImageFont
from alive_progress import alive_bar
def initImg(width, height, bg, font='fonts/FatBoyVeryRoundItalic.ttf', size = 41):
    #creating B/W image
    img = Image.new('L', (width, height), color=bg)
    fnt = ImageFont.truetype(font, 41)
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
                    if textWidth(lastLine(string)+newNum[:2], cacheTable)<=(width+30):
                        string+=newNum[:1]
                        newNum = newNum[1:]
                        bar(text = "dict", incr=1)
                    #elif drawer.textsize(lastLine(string)+newNum[:1], font)[0] <= width:
                    #    #if it reaches the end of the line fast way, then we need
                    #    #to check for missing ending with trusted and slow way
                    #    string+=newNum[:1]
                    #    newNum = newNum[1:]
                    #    bar(text="non-dict", incr=1)
                    else:
                        string += "\n"
                        lines += 1
                        innerFinished = True
                else:
                    newNum += str(count) + " "
                    count += 1
            if lines >= maxLines:
                finished = True
        return string, count-1

def cacheTable(drawer, font, charsToCache):
    cacheTable = dict()
    for char in charsToCache:
        cacheTable[char]=drawer.textsize(char, font)[0]
    print("Created cache table")
    return cacheTable

def getMaxLines(drawer, font, height):
    i = 0
    pxs = 0
    print("Calculating lines quantity...")
    with alive_bar(height) as bar:
        while True:
            my_height = drawer.textsize("0\n"*i, font)[1]
            if my_height<=height:
                i += 1
                bar(incr=my_height-pxs)
                pxs = my_height
            else:
                bar(incr=height-pxs)
                break
    print("Calculated max number of lines. Its", i, "lines.")
    return i

def printText(string, drawer, font, colors, cacheTable):
    print("Printing text on image...")
    lines = string.split("\n")
    index = 0
    indexinl = 0
    with alive_bar(len(string.replace("\n", ""))) as bar:
        for l, line in enumerate(lines):
            if l == 1:
                h = drawer.textsize("0000"*(l), font)[1]
            else:
                h = drawer.textsize("0000000\n00000000"*(l-1), font)[1]
            indexinl = 0
            for char in line:
                w = textWidth(line[:indexinl], cacheTable)
                drawer.text((w, h), char, font=font, fill=colors[index])
                index += 1
                indexinl += 1
                bar()



def save(img, filename):
    print("Saving...")
    img.save(filename)
    print("Saved as", filename)