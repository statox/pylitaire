from PIL import Image, ImageTk

class Card():
    def __init__(self, symbol, value):
        # Members specifics to the game
        self.symbol    = symbol
        self.value     = value
        self.facedown  = True
        self.color     = "R"
        if (symbol == "S" or symbol == "C"):
            self.color = "B"

        # GUI members
        pathToImage              = "../img/" + self.symbol + self.value + ".bmp"
        imageFaceUp              = Image.open(pathToImage)
        self.photoFaceUp         = ImageTk.PhotoImage(imageFaceUp)
        self.photoFaceUpCropped  = ImageTk.PhotoImage(imageFaceUp.crop((0, 0, imageFaceUp.size[0], imageFaceUp.size[1]/4)))

    def setFaceDown(self, value):
        self.facedown = value
        
    def __str__(self):
        if self.facedown:
            return  "\033[90m" + "## " +  "\033[0m"
        else:
            if (self.color == "R"):
                colorString = "\033[31m"
            else:
                colorString = ""
            if (self.value == "10"):
                offsetString = ""
            else:
                offsetString = " "
            return colorString + self.value + self.symbol + offsetString + "\033[0m"

    def __eq__(self, other):
        if isinstance(other, Card):
            return (self.symbol == other.symbol and
                   self.value == other.value)
        return NotImplemented

    def __hash__(self):
        return hash(self.symbol + self.value)
