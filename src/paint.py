import random
random.seed(None)

class Paint:
    def __init__(self):
        self.value=255
    def use(self):
        percent = float(random.randrange(15, 60)/1000)
        self.value -= int(self.value*percent)
    def refill(self):
        self.value = 255
    def get_value(self):
        return self.value

def getColors(string, bg):
    print("Generating color table")
    string = string.replace("\n", "")
    paint = Paint()
    colors = []

    if bg >= 255:
        for i in string:
            colors.append(255)
        return colors

    for i in string:
        colors.append(0)
        
    for i, char in enumerate(string):
        if char == " ":
            colors[i] = 255
            if paint.get_value()<=120+bg:
                paint.refill()
        else:
            colors[i] = paint.get_value()
            paint.use()
    print("Generated color table")
    return colors



