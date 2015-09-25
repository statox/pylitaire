from functools import partial
from boardFrame import BoardFrame
from board import Board
from Tkinter import *
from pubsub import pub

class BoardController:
    def __init__(self):
        self.root = Tk()
        w, h = self.root.winfo_screenwidth()/2, self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))

        self.boardFrame = BoardFrame(self.root)
        self.board = Board()
        self.boardFrame.pack(side=TOP, fill=BOTH, expand=True)

        self.refreshGui()

        # Define commands linked to the view buttons
        self.defineCardsActions()
        # Subscribes to event from the board to know when to refresh the GUI 
        pub.subscribe(self.listenerGui, 'refreshGUITopic')
        # Subscribes to event when a card is clicked
        pub.subscribe(self.listenerClick, 'cardClicked')
        self.clickCount = 0
        self.prevClickedCard = None

    # Listener for GUI refresh
    # When the GUI is refreshed we also need to re-bind the cards buttons
    # to the right actions
    def listenerGui(self):
        self.refreshGui()
        self.defineCardsActions()

    # Listen for cards which are clicked and either keep the card in memory
    # or call the board method to choose what to do
    def listenerClick(self, cardClicked):
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
