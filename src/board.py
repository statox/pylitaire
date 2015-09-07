from random import shuffle
from card import Card

class Board:
    def __init__(self):
        self.values = ['1','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.symbols = ['H', 'S', 'C', 'D']

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

            self.PlayingStacks[stack][-1].facedown = False

        # Make the last card of the stock visible
        self.stock[-1].facedown = False
            

    def pickCardFromStock(self):
        # If stock gets empty, recycle the waste
        if (len(self.stock) == 0):
            while (len(self.waste) > 0):
                self.stock.append(self.waste.pop())
                self.stock[-1].facedown = True
            self.stock[-1].facedown = False

        card = self.stock.pop()
        self.waste.append(card)
        if (len(self.stock) > 0):
            self.stock[-1].facedown = False

    def moveCardFromWaste(self, choice):
        cardValue = self.values.index(self.waste[-1].value)
        # If we try to put the card on the tableau check the color isnt the same
        # and the values are following
        if (choice.isdigit() and int(choice) >= 1 and int(choice) <= 7):
            destination = self.PlayingStacks[int(choice) - 1]
            if (self.waste[-1].color == destination[-1].color or 
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

            print ("Card        : " + cardValue.__str__()        + "\t" + self.waste[-1].symbol.__str__())
            print ("Destination : " + len(destination).__str__() + "\t" + choice.__str__())
            if (cardValue != len(destination) or
                self.waste[-1].symbol != choice):
                print("Wrong color or wrong value")
                return -1

        # If all conditions are ok move the card
        destination.append(self.waste.pop())

    def moveCardFromTableau(self, card, choice):
        # card.facedown = False
        # print("looking for card " + card.__str__())

        # # Get the list of cards to move (the list can contain only one card)
        # pileIndex = -1
        # for s in self.PlayingStacks:
            # if (card in s):
                # pileIndex = self.PlayingStacks.index(s)
                # cardIndex = s.index(card)
                # cardsList = s[cardIndex:-1+1]
        # if (pileIndex != -1):
            # print("found in pile: " + pileIndex.__str__())
            # print("index in pile: " + cardIndex.__str__())
            # print("list of cards: ")
            # for c in cardsList:
                # print(c.__str__())
        print("not implemented yet")
        
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

        str = str + "H: "
        if (len(self.H) > 0): str = str + self.H[-1].__str__()

        str = str + '\n' + "C: ".__str__()
        if (len(self.C) > 0): str = str + self.C[-1].__str__()

        str = str + '\n' + "S: ".__str__()
        if (len(self.S) > 0): str = str + self.S[-1].__str__()

        str = str + '\n' + "D: ".__str__()
        if (len(self.D) > 0): str = str + self.D[-1].__str__()

        str =  str + '\n' +"stacks: "
        for s in self.PlayingStacks:
            str = str + "\n"
            for card in s:
                str = str + card.__str__() + '\t'

        return str


