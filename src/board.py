from random import shuffle
from card import Card
from boardFrame import BoardFrame
from pubsub import pub

class Board():
    # def __init__(self, GUIMaster):
    def __init__(self, boardFrame):
        self.values      = ['1','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.symbols     = ['H', 'S', 'C', 'D']
        # self.boardFrame  = BoardFrame(GUIMaster)
        self.boardFrame  = boardFrame

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

        # generate empyt waste
        self.waste = []

        # generate piles used to play
        self.PlayingStacks = [[], [], [], [], [], [], []]
        for stack in range (0, 7):
            for index in range (-1, stack):
                card = self.stock.pop()
                self.PlayingStacks[stack].append(card)

            self.PlayingStacks[stack][-1].setFaceDown(False)

        # Update GUI
        # self.boardFrame.updateGUI(self)
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
        # self.boardFrame.updateGUI(self)
        pub.sendMessage('refreshGUITopic')

    def moveCardFromFoundation(self, choosenFoundation, choosenDestination):
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
            print ("No card to move")
            return -1
        else:
            card = foundation[-1]
            cardValue = self.values.index(card.value) 

        # check if we can move the card
        if (choosenDestination.isdigit() and 
            int(choosenDestination) >= 1 and int(choosenDestination) <= 7):
            destination = self.PlayingStacks[int(choosenDestination) - 1]
            if (len(destination) == 0):
                if (card.value != "K"):
                    print ("You can only move a king here")
                    return -1
            elif (card.color == destination[-1].color or 
                  cardValue != self.values.index(destination[-1].value)-1):
                print("Wrong color or wrong value")
                return -1
        else:
            print("Incorrect choice of pile")
            return -1

        destination.append(foundation.pop())
        # self.boardFrame.updateGUI(self)
        pub.sendMessage('refreshGUITopic')
        return 0

    def moveCardFromWaste(self, choice):
        cardValue = self.values.index(self.waste[-1].value)
        # If we try to put the card on the tableau check the color isnt the same
        # and the values are following
        if (choice.isdigit() and int(choice) >= 1 and int(choice) <= 7):
            destination = self.PlayingStacks[int(choice) - 1]
            if (len(destination) == 0):
                if (self.waste[-1].value != "K"):
                    print ("You can only move a king here")
                    return -1
            elif (self.waste[-1].color == destination[-1].color or 
                  cardValue != self.values.index(destination[-1].value)-1):
                print("Wrong color or wrong value")
                return -1
        # If we try to put the card on the foundations
        else:
            if (choice == "H"):
                destination = self.H
            elif (choice == "S"):
                destination = self.S
            elif (choice == "D"):
                destination = self.D
            elif (choice == "C"):
                destination = self.C
            else:
                return -1

            print ("Card        : " + cardValue.__str__()        + "\t" 
                   + self.waste[-1].symbol.__str__())
            print ("Destination : " + len(destination).__str__() + "\t" 
                   + choice.__str__())
            if (cardValue != len(destination) or
                self.waste[-1].symbol != choice):
                print("Wrong color or wrong value")
                return -1

        # If all conditions are ok move the card
        destination.append(self.waste.pop())
        # self.boardFrame.updateGUI(self)
        pub.sendMessage('refreshGUITopic')

    def moveCardFromTableau(self, card, choice):
        card.setFaceDown(False)
        cardValue = self.values.index(card.value)
        print("looking for card " + card.__str__())
        print("To move to " + choice.__str__())

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
            print ("This card cant be moved")
            pub.sendMessage('refreshGUITopic')
            return -1

        print("Card found in list : " + pileIndex.__str__() + "[" 
              + cardIndex.__str__() + "/" + len(s).__str__() + "]")
        print("Number of card to move " + nbOfCards.__str__())
        
        # Try to move to the tableau
        if (choice.isdigit() and int(choice) >= 1 and int(choice) <= 7):
            destination = self.PlayingStacks[int(choice) - 1]
            # Move only king if the pile is empty
            if (len(destination) == 0):
                if (card.value != "K"):
                    print("You can only move a king here")
                    pub.sendMessage('refreshGUITopic')
                    return -1
            # is the pile isnt empty check the values and colors
            elif (card.color == destination[-1].color or 
                  cardValue != self.values.index(destination[-1].value)-1):
                print("Wrong color or wrong value")
                pub.sendMessage('refreshGUITopic')
                return -1
        # Try to move in to the foundations
        else:
            if (choice == "H"):
                destination = self.H
            elif (choice == "S"):
                destination = self.S
            elif (choice == "D"):
                destination = self.D
            elif (choice == "C"):
                destination = self.C
            else:
                pub.sendMessage('refreshGUITopic')
                return -1

            # Fail if we try to put several cards at the time in a foundation
            if (nbOfCards != 1):
                print("You can move more than one card here")
                pub.sendMessage('refreshGUITopic')
                return -1
            # Checks on the values and colors
            if (cardValue != len(destination) or
                card.symbol != choice):
                print("Wrong color or wrong value")
                pub.sendMessage('refreshGUITopic')
                return -1

        # Actually move the cards
        for c in range(cardIndex, len(s)):
            print("pop index " + c.__str__())
            destination.append(s.pop(cardIndex))

        # Reveal the card which was before the moved one(s)
        if (len(s) > 0):
            s[-1].setFaceDown(False)

        pub.sendMessage('refreshGUITopic')
        return 0


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


