from PIL import ImageColor
def getcolor(hexcode):
    return ImageColor.getcolor(hexcode, "RGB")
class colors:
    def __init__(self):
        self.bgColor = getcolor("#FCBF49")
        self.gridColors = [
            getcolor("#EAE2B7"),
            getcolor("#003049"),
            getcolor("#D62828"),
            getcolor("#5DF95D"),
            getcolor("#F48749"),
            getcolor("#4FBDBA"),
            getcolor("#9F959A")
        ]
        self.darkerPath = getcolor("#AE460A")
        self.textFG = getcolor("#284483")
        self.textBG = getcolor("#F48749")

