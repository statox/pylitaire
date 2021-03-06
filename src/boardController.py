from functools   import partial
from boardFrame  import BoardFrame
from board       import Board
from Tkinter     import *
from pubsub      import pub
from ai          import AI

class BoardController:
    def __init__(self):
        self.root = Tk()
        w, h = self.root.winfo_screenwidth()/2, self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))

        self.boardFrame = BoardFrame(self.root)
        self.board = Board()
        self.boardFrame.pack(side=TOP, fill=BOTH, expand=True)
        self.ai = AI()

        # Define commands linked to the view buttons
        self.defineCardsActions()
        self.boardFrame.possibleMovesButton.configure(command=self.showPossibleMoves)
        # Subscribes to event from the board to know when to refresh the GUI 
        pub.subscribe(self.listenerGui, 'refreshGUITopic')
        # Subscribes to event when a card is clicked
        pub.subscribe(self.listenerClick, 'cardClicked')
        self.clickCount = 0
        self.prevClickedCard = None

        # Show board for the first time
        pub.sendMessage('refreshGUITopic')

    # Listener for GUI refresh
    # When the GUI is refreshed we also need to re-bind the cards buttons
    # to the right actions
    def listenerGui(self):
        self.refreshGui()
        self.defineCardsActions()
        if (self.ai.willWin(self.board)):
            print("PLayer will win")


    # Listen for cards which are clicked and either keep the card in memory
    # or call the board method to choose what to do
    def listenerClick(self, cardClicked):
        # If the stock card is clicked don't wait from a second card
        if (cardClicked == "stock"):
            self.clickCount = 0
            self.board.chooseMovement(cardClicked)
            return 0

        self.clickCount += 1
        if (self.clickCount == 1):
            self.prevClickedCard = cardClicked
        elif (self.clickCount == 2):
            self.clickCount = 0
            self.board.chooseMovement(self.prevClickedCard, cardClicked)
        else:
            return 0

    def startGame(self):
        self.root.mainloop()

    def refreshGui(self):
        self.boardFrame.updateGUI(self.board)

    def showPossibleMoves(self):
        possibleMoves = self.ai.possibleMoves(self.board)
        movesButtons = {}
        for origin, destination in possibleMoves:
            # Get button corresponding to card orgin
            if (len(self.board.H)>0 and origin == self.board.H[-1]):
                buttonOrigin = self.boardFrame.HButton
            elif (len(self.board.S)>0 and origin == self.board.S[-1]):
                buttonOrigin = self.boardFrame.SButton
            elif (len(self.board.C)>0 and origin == self.board.C[-1]):
                buttonOrigin = self.boardFrame.CButton
            elif (len(self.board.D)>0 and origin == self.board.D[-1]):
                buttonOrigin = self.boardFrame.DButton
            elif (len(self.board.waste)>0 and origin == self.board.waste[-1]):
                buttonOrigin = self.boardFrame.wasteButton
            else:
                buttonOrigin = self.boardFrame.cardButtons[origin]

            # Get button corresponding to card destination
            if (destination == "H"):
                buttonDestination = self.boardFrame.HButton
            elif (destination == "S"):
                buttonDestination = self.boardFrame.SButton
            elif (destination == "C"):
                buttonDestination = self.boardFrame.CButton
            elif (destination == "D"):
                buttonDestination = self.boardFrame.DButton
            else:
                buttonDestination = self.boardFrame.cardButtons[destination]

            if not buttonOrigin in movesButtons:
                movesButtons[buttonOrigin] = []

            movesButtons[buttonOrigin].append(buttonDestination)

        self.boardFrame.showPossibleMoves(movesButtons)

    def defineCardsActions(self):
        # This dictionnary contains the cards and the command to bound
        cardActions = {}
        bf = self.boardFrame
        # Cards from stock and waste
        cardActions[self.boardFrame.stockButton]=partial(pub.sendMessage, 'cardClicked', cardClicked="stock")
        cardActions[self.boardFrame.wasteButton]=partial(pub.sendMessage, 'cardClicked', cardClicked="W")

        # Cards from foundations
        cardActions[bf.HButton]=partial(pub.sendMessage, 'cardClicked', cardClicked="H")
        cardActions[bf.CButton]=partial(pub.sendMessage, 'cardClicked', cardClicked="C")
        cardActions[bf.SButton]=partial(pub.sendMessage, 'cardClicked', cardClicked="S")
        cardActions[bf.DButton]=partial(pub.sendMessage, 'cardClicked', cardClicked="D")

        # cards from the tableau
        for card in bf.cardButtons.keys():
            # find the pile in which the card is
            pileIndex = -1
            for s in self.board.PlayingStacks:
                if (card in s):
                    pileIndex = self.board.PlayingStacks.index(s)
                    break

            cardActions[bf.cardButtons[card]]= partial(pub.sendMessage, 'cardClicked', cardClicked=card)

        # Empty tableau piles
        for frame, button in bf.tableauFirstCardButtons.items():
            cardActions[button] = partial(pub.sendMessage, 'cardClicked', cardClicked=frame)


        # actually bind the buttons
        for button in cardActions:
            button.configure(command=cardActions[button])
        return 0
