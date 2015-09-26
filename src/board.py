from random import shuffle
from card import Card
from pubsub import pub

class Board():
    def __init__(self):
        # Values and symbols of the card which will be created
        self.values      = ['1','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.symbols     = ['H', 'S', 'C', 'D']

        # Generate the stock
        self.stock = []
        for symbol in self.symbols:
            for value in self.values:
                self.stock.append(Card(symbol, value))
        shuffle(self.stock)

        # Generate the waste
        self.waste = []

        # generate empty piles for each color
        self.H = []
        self.C = []
        self.S = []
        self.D = []

        # generate empty waste
        self.waste = []

        # generate tableau piles used to play
        self.PlayingStacks = [[], [], [], [], [], [], []]
        for stack in range (0, 7):
            for index in range (-1, stack):
                card = self.stock.pop()
                self.PlayingStacks[stack].append(card)

            self.PlayingStacks[stack][-1].setFaceDown(False)

        # Update GUI
        pub.sendMessage('refreshGUITopic')


    def pickCardFromStock(self):
        return 0

    def moveCardFromFoundation(self, choosenFoundation, destinationCard):
        choosenDestination = self.getCardPosition(destinationCard)

        # Get the foundation to treat
        if (choosenFoundation == "H"):
            foundation = self.H
        elif (choosenFoundation == "S"):
            foundation = self.S
        elif (choosenFoundation == "D"):
            foundation = self.D
        elif (choosenFoundation == "C"):
            foundation = self.C
        else:
            return -1

        # check that there is a card to move
        if (len(foundation) < 1):
            # print ("No card to move")
            return -1
        else:
            card = foundation[-1]
            cardValue = self.values.index(card.value) 

        # check if we can move the card
        if ( choosenDestination >= 0 and choosenDestination <= 6):
            destination = self.PlayingStacks[choosenDestination]
            if (len(destination) == 0):
                if (card.value != "K"):
                    # print ("You can only move a king here")
                    return -1
            elif (card.color == destination[-1].color or 
                  cardValue != self.values.index(destination[-1].value)-1):
                # print("Wrong color or wrong value")
                return -1
        else:
            # print("Incorrect choice of pile")
            return -1

        return 0

    def moveCardFromWaste(self, destinationCard):
        wasteCardValue      = self.values.index(self.waste[-1].value)
        choosenDestination  = self.getCardPosition(destinationCard)

        # If we try to put the card on the tableau check the color isnt the same
        # and the values are following
        if (choosenDestination >= 0 and choosenDestination <= 6):
            destination = self.PlayingStacks[choosenDestination]
            if (len(destination) == 0):
                if (self.waste[-1].value != "K"):
                    # print ("You can only move a king here")
                    return -1
            elif (self.waste[-1].color == destination[-1].color or 
                  wasteCardValue != self.values.index(destination[-1].value)-1):
                # print("Wrong color or wrong value")
                return -1
        # If we try to put the card on the foundations
        else:
            if (choosenDestination == "H"):
                destination = self.H
            elif (choosenDestination == "S"):
                destination = self.S
            elif (choosenDestination == "D"):
                destination = self.D
            elif (choosenDestination == "C"):
                destination = self.C
            else:
                return -1

            if (wasteCardValue != len(destination) or
                self.waste[-1].symbol != choosenDestination):
                # print("Wrong color or wrong value")
                return -1

        return 0

    def moveCardFromTableau(self, card, destinationCard):
        card.setFaceDown(False)
        cardValue = self.values.index(card.value)

        choosenDestination  = self.getCardPosition(destinationCard)

        # Get the list of cards to move (the list can contain only one card)
        pileIndex = -1
        for s in self.PlayingStacks:
            if (card in s):
                pileIndex = self.PlayingStacks.index(s)
                cardIndex = s.index(card)
                nbOfCards = len(s) - cardIndex
                break
        # Fail if we select a card which isnt in the tableau
        if (pileIndex == -1):
            # print ("This card cant be moved")
            return -1
        
        # Try to move to the tableau
        if (choosenDestination >= 0 and choosenDestination <= 6):
            destination = self.PlayingStacks[choosenDestination]
            # Move only king if the pile is empty
            if (len(destination) == 0):
                if (card.value != "K"):
                    # print("You can only move a king here")
                    return -1
            # is the pile isnt empty check the values and colors
            elif (card.color == destination[-1].color or 
                  cardValue != self.values.index(destination[-1].value)-1):
                # print("Wrong color or wrong value")
                return -1
        # Try to move in to the foundations
        else:
            if (choosenDestination == "H"):
                destination = self.H
            elif (choosenDestination == "S"):
                destination = self.S
            elif (choosenDestination == "D"):
                destination = self.D
            elif (choosenDestination == "C"):
                destination = self.C
            else:
                return -1

            # Fail if we try to put several cards at the time in a foundation
            if (nbOfCards != 1):
                # print("You can move more than one card here")
                return -1
            # Checks on the values and colors
            if (cardValue != len(destination) or
                card.symbol != choosenDestination):
                # print("Wrong color or wrong value")
                return -1

        return 0

    # Help to determine where is a card of the board
    # To have a consistent behavior with empty emplacements the function
    # can also take a string as argument representing the empty place
    # Returns:
    # [0-6]: If the card is face up in a tableau pile
    # ["H", "S", "C", "D"]: If the card is the last one in a foundation
    # "W": If the card is the last one in the waste
    # -1: otherwise
    def getCardPosition(self, card):
        if ( card is not None ):
            if card.__str__() in {"W", "H", "S", "C", "D", "0", "1", "2", "3", "4", "5", "6"}:
                return card
            if ( len(self.waste) and self.waste[-1] == card ):
                return "W"
            elif ( len(self.H)!=0 and self.H[-1] == card ):
                return "H"
            elif ( len(self.S)!=0 and self.S[-1] == card ):
                return "S"
            elif ( len(self.C)!=0 and self.C[-1] == card ):
                return "C"
            elif ( len(self.D)!=0 and self.D[-1] == card ):
                return "D"
            else:
                index = -1
                for pile in self.PlayingStacks:
                    index += 1
                    for c in pile:
                        if (c == card and not c.facedown):
                            return index
        return -1

    # Takes a position returned by self.getCardPosition
    # returns the corresponding object on the board
    def getPositionObject(self, position):
        if (position == "H"):
            return self.H
        elif (position == "S"):
            return self.S
        elif (position == "D"):
            return self.D
        elif (position == "C"):
            return self.C
        elif (position == "W"):
            return self.waste
        elif (position >= 0 and position <= 6):
            return self.PlayingStacks[position]
        else:
            return self.stock

        return None

    # Takes a card to move and a card where to move the first one
    # Depending on the position of the cardOrigin, call the corresponding
    # movement method
    def chooseMovement(*args):
        if (len(args)>0):
            self = args[0]

        if (len(args)>1):
            cardOrigin       = args[1]
            cardDestination  = None

        if (len(args)>2):
            cardDestination  = args[2]

        if (len(args)<=1 or len(args)>3):
            return -1

        cardPosition = self.getCardPosition(cardOrigin)

        movePossible = -1
        if (cardPosition in {"H", "S", "C", "D"}):
            movePossible = self.moveCardFromFoundation(cardOrigin, cardDestination)
        elif (cardPosition == "W"):
            movePossible = self.moveCardFromWaste(cardDestination)
        elif (cardPosition >= 0 and cardPosition <= 6):
            movePossible = self.moveCardFromTableau(cardOrigin, cardDestination)
        else:
            movePossible = self.pickCardFromStock()

        if (movePossible == 0):
            self.moveCard(cardOrigin, cardDestination)
        return 1

    def moveCard(*args):
        if (len(args)>0):
            self = args[0]
        if (len(args)>1):
            cardOrigin     = args[1]
            if (cardOrigin != "stock"):
                symboleOrigin  = self.getCardPosition(cardOrigin)
                origin         = self.getPositionObject(symboleOrigin)
            else:
                symboleOrigin      = "stock"
                origin             = self.stock
                symbolDestination  = "W"
                destination        = self.waste
        if (len(args)>2):
            cardDestination    = args[2]
            symbolDestination  = self.getCardPosition(cardDestination)
            destination        = self.getPositionObject(symbolDestination)
        if (len(args)<=1 or len(args)>3):
            return -1

        # Card in one the the foundations
        if (symboleOrigin in [ "H", "S", "C", "D" ]):
            destination.append(origin.pop())
        # Card in the waste
        elif (symboleOrigin == "W"):
            destination.append(origin.pop())
        # Card in the tableau
        elif (symboleOrigin >= 0 and symboleOrigin <= 6):
            # Get the position of the card in its pile
            cardIndex = origin.index(cardOrigin)
            # Move the card (and the ones below)
            for c in range(cardIndex, len(origin)):
                destination.append(origin.pop(cardIndex))
            # Reveal the card which was before the moved one(s)
            if (len(origin) > 0):
                origin[-1].setFaceDown(False)
        # Card in the stock
        elif (symboleOrigin == "stock"):
            # If stock gets empty, recycle the waste
            if (len(self.stock) == 0):
                while (len(self.waste) > 0):
                    self.stock.append(self.waste.pop())
                    self.stock[-1].setFaceDown(True)
                self.stock[-1].setFaceDown(False)

            card = self.stock.pop()
            self.waste.append(card)
            if (len(self.waste) > 0):
                self.waste[-1].setFaceDown(False)

        pub.sendMessage('refreshGUITopic')
        return 1

    def __str__(self):
        str = "stock: "
        card = "  "
        if (len(self.stock) > 0):
            card = self.stock[-1].__str__()
        str = str + card + "\t[" + len(self.stock).__str__() + "]" + '\n'

        str = str + "waste: "
        card = "  "
        if (len(self.waste) > 0):
            card = self.waste[-1].__str__()
        str = str + card + "\t[" + len(self.waste).__str__() + "]" + '\n'

        str = str + "foundations: " + '\n'
        str = str + "H: "
        if (len(self.H) > 0): str = str + self.H[-1].__str__()

        str = str + '\n' + "C: ".__str__()
        if (len(self.C) > 0): str = str + self.C[-1].__str__()

        str = str + '\n' + "S: ".__str__()
        if (len(self.S) > 0): str = str + self.S[-1].__str__()

        str = str + '\n' + "D: ".__str__()
        if (len(self.D) > 0): str = str + self.D[-1].__str__()

        str =  str + '\n' +"stacks: "
        cpt = 0
        for s in self.PlayingStacks:
            cpt += 1
            str = str + "\n" + cpt.__str__() + ": "
            for card in s:
                str = str + card.__str__() + " "

        return str


