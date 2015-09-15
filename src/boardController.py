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
        pub.subscribe(self.listener1, 'refreshGUITopic')

    # Listener for GUI refresh
    # When the GUI is refreshed we also need to re-bind the cards buttons
    # to the right actions
    def listener1(self):
        self.refreshGui()
        self.defineCardsActions()

    def startGame(self):
        self.root.mainloop()

    def refreshGui(self):
        self.boardFrame.updateGUI(self.board)

    def defineCardsActions(self):
        self.boardFrame.stockButton.configure(command=self.pickCardFromStock)
        self.boardFrame.wasteButton.configure(command=self.moveCardFromWaste)
        self.defineTableauButtonActions()

    def pickCardFromStock(self):
        self.board.pickCardFromStock()

    def moveCardFromWaste(self):
        self.boardFrame.HButton.configure(command=lambda: self.board.moveCardFromWaste("H"))
        self.boardFrame.CButton.configure(command=lambda: self.board.moveCardFromWaste("C"))
        self.boardFrame.SButton.configure(command=lambda: self.board.moveCardFromWaste("S"))
        self.boardFrame.DButton.configure(command=lambda: self.board.moveCardFromWaste("D"))

        frames = self.boardFrame.tableauFrames
        for index in range (0, 7):
            if len(frames[index].winfo_children()) > 0:
                child = frames[index].winfo_children()[-1]
                command = partial(self.board.moveCardFromWaste, (index +1).__str__())
                child.configure(command=command)

    def defineTableauButtonActions(self):
        for key in self.boardFrame.cardButtons.keys():
            button  = self.boardFrame.cardButtons[key]
            command = partial(self.moveCardFromTableau, key)
            button.configure(command=command)

    def moveCardFromTableau(self, card):
        # bind card from the foundations to moveFromTableau
        commandH = partial(self.board.moveCardFromTableau, card, "H")
        commandC = partial(self.board.moveCardFromTableau, card, "C")
        commandS = partial(self.board.moveCardFromTableau, card, "S")
        commandD = partial(self.board.moveCardFromTableau, card, "D")

        self.boardFrame.HButton.configure(command=commandH)
        self.boardFrame.CButton.configure(command=commandC)
        self.boardFrame.SButton.configure(command=commandS)
        self.boardFrame.DButton.configure(command=commandD)

        # bind cards of the tableau to moveFromTableau
        for key in self.boardFrame.cardButtons.keys():
            # find the pile in which the card is
            pileIndex = -1
            for s in self.board.PlayingStacks:
                if (key in s):
                    pileIndex = self.board.PlayingStacks.index(s)
                    break

            button  = self.boardFrame.cardButtons[key]
            command = partial(self.board.moveCardFromTableau, card, (pileIndex + 1).__str__())
            button.configure(command=command)
