from PIL import Image, ImageDraw, ImageFont
from alive_progress import alive_bar

def initImg(width, height, bg, font='fonts/FatBoyVeryRoundItalic.ttf', size = 41, verbose=False):
    #creating B/W image
    img = Image.new('L', (width, height), color=bg)
    fnt = ImageFont.truetype('fonts/FatBoyVeryRoundItalic.ttf', 41)
    d = ImageDraw.Draw(img)
    if verbose:
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

def wrap(width, maxLines, cacheTable, drawer, font, count, verbose=False):
    def logic(bar, count, maxLines):
        string = ""
        newNum = ""
        lines = 0
        finished = False

        while not finished: 
            innerFinished = False
            while not innerFinished:
                if len(newNum)>0:  
                    if textWidth(lastLine(string)+newNum[:2], cacheTable)<=(width+30):
                        string+=newNum[:1]
                        newNum = newNum[1:]
                        bar(text = "dict", incr=1)
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
        
    if verbose:
        print("Creating text...")
        with alive_bar() as bar:
            return logic(bar, count, maxLines)
    else:
        def bar(**kwargs):
            pass
        return logic(bar, count, maxLines)

def cacheTable(drawer, font, charsToCache, verbose=False):
    cacheTable = dict()
    for char in charsToCache:
        cacheTable[char]=drawer.textsize(char, font)[0]
    if verbose:
        print("Created cache table")
    return cacheTable

def getMaxLines(drawer, font, height, verbose=False):
    def logic(bar):
        i = 0
        pxs = 0
        while True:
            my_height = drawer.textsize("0\n"*i, font)[1]
            if my_height<=height:
                i += 1
                bar(incr=my_height-pxs)
                pxs = my_height
            else:
                bar(incr=height-pxs)
                break
        return i
        
    if verbose:
        print("Calculating lines quantity...")
        with alive_bar(height) as bar:
            i = logic(bar)
        print("Calculated max number of lines. Its", i, "lines.")
        
    else:
        def bar(**kwargs):
            pass
        i = logic(bar)
    return i

def printText(string, drawer, font, colors, cacheTable, verbose = False):
    def logic(bar):
        lines = string.split("\n")
        index = 0
        indexinl = 0
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

    if verbose:
        print("Printing text on image...")
        with alive_bar(len(string.replace("\n", ""))) as bar:
            logic(bar)
    else:
        def bar(**kwargs):
            pass
        logic(bar)

def save(img, filename, verbose = False):
    if verbose:
        print("Saving...")
    img.save(filename)
    if verbose:
        print("Saved as", filename)
