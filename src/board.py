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

        # Update GUI
        pub.sendMessage('refreshGUITopic')

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

        destination.append(foundation.pop())

        # Update GUI
        pub.sendMessage('refreshGUITopic')
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

        # If all conditions are ok move the card
        destination.append(self.waste.pop())

        # Update GUI
        pub.sendMessage('refreshGUITopic')

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
            pub.sendMessage('refreshGUITopic')
            return -1
        
        # Try to move to the tableau
        if (choosenDestination >= 0 and choosenDestination <= 6):
            destination = self.PlayingStacks[choosenDestination]
            # Move only king if the pile is empty
            if (len(destination) == 0):
                if (card.value != "K"):
                    # print("You can only move a king here")
                    pub.sendMessage('refreshGUITopic')
                    return -1
            # is the pile isnt empty check the values and colors
            elif (card.color == destination[-1].color or 
                  cardValue != self.values.index(destination[-1].value)-1):
                # print("Wrong color or wrong value")
                pub.sendMessage('refreshGUITopic')
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
                pub.sendMessage('refreshGUITopic')
                return -1

            # Fail if we try to put several cards at the time in a foundation
            if (nbOfCards != 1):
                # print("You can move more than one card here")
                pub.sendMessage('refreshGUITopic')
                return -1
            # Checks on the values and colors
            if (cardValue != len(destination) or
                card.symbol != choosenDestination):
                # print("Wrong color or wrong value")
                pub.sendMessage('refreshGUITopic')
                return -1

        # Actually move the cards
        for c in range(cardIndex, len(s)):
            destination.append(s.pop(cardIndex))

        # Reveal the card which was before the moved one(s)
        if (len(s) > 0):
            s[-1].setFaceDown(False)

        pub.sendMessage('refreshGUITopic')
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

    # Takes a card to move and a card where to move the first one
    # Depending on the position of the cardOrigin, call the corresponding
    # movement method
    def chooseMovement(*args):
        print("args len: " + len(args).__str__() + "  args: " + args.__str__())
        if (len(args)>0):
            self = args[0]
        if (len(args)>1):
            cardOrigin = args[1]
        if (len(args)>2):
            cardDestination = args[2]
        if (len(args)<=1 or len(args)>3):
            print("Invalid number of argsuments")
            return -1

        print("choos movement: " + cardOrigin.__str__() +
                " =>  " + cardDestination.__str__())

        cardPosition = self.getCardPosition(cardOrigin)

        if (cardPosition in {"H", "S", "C", "D"}):
            print("Move from foundations")
            self.moveCardFromFoundation(cardOrigin, cardDestination)
            return 1
        elif (cardPosition == "W"):
            print("Move from waste")
            self.moveCardFromWaste(cardDestination)
            return 1
        elif (cardPosition >= 0 and cardPosition <= 6):
            print("Move from tableau")
            self.moveCardFromTableau(cardOrigin, cardDestination)
            return 1
        else:
            print("pick from stock")
            self.pickCardFromStock()
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


