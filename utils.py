from PIL import Image, ImageDraw, ImageFont
from alive_progress import alive_bar
def initImg(width, height, font='FatBoyVeryRoundItalic.ttf', size = 41):
    #creating B/W image
    img = Image.new('L', (width, height), color=0)
    fnt = ImageFont.truetype('FatBoyVeryRoundItalic.ttf', 41)
    d = ImageDraw.Draw(img)
    print("Created image")
    return img, fnt, d

def textWidth(string, cacheTable):
	output = 0
	for char in string:
		output += cacheTable[char]
	return output

def wrap(text,containerWidth, cacheTable, drawer, font):
    print("Creating text...")
    lines = []
    finished = False
    line = 0
    with alive_bar(len(text)) as bar:
        while not finished:
            newline = ""
            innerFinished = False
            while not innerFinished:
                if (textWidth(newline+text[:1], cacheTable)<= containerWidth) and len(text)>=1:
                    newline+=text[:1]
                    text = text[1:]
                    bar(incr=1)
                elif (drawer.textsize(newline+text[:1], font)[0] <= containerWidth) and len(text)>=1:
                    #if it reaches the end of the line fast way, then we need
                    #to check for missing ending with trusted and slow way
                    newline+=text[:1]
                    text = text[1:]
                    bar(text="non-dict", incr=1)
                else:
                    innerFinished = True
            if len(newline) > 0:
                lines.append(newline)
                line = line + 1
            else:
                finished = True
        return(lines)

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

def printText(wrapped, d, fnt):
    print("Printing lines...")
    h = 0
    with alive_bar(len(wrapped), force_tty=True) as bar:
        for i in wrapped:
            d.text((5, h), i, font=fnt, fill=255)
            h += d.textsize(i, fnt)[1]+1
            bar()

def save(img, filename):
    print("Saving...")
    img.save(filename)
    print("Saved")