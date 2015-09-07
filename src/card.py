class Card:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value   = value
        self.facedown = True
        self.color = "R"
        if (symbol == "S" or symbol == "C"):
            self.color = "B"
        
    def __str__(self):
        if self.facedown:
            return "##"
        else:
            return self.value + self.symbol + "-" + self.color

    def __eq__(self, other):
        if isinstance(other, Card):
            return (self.symbol == other.symbol and
                   self.value == other.value)
        return NotImplemented
