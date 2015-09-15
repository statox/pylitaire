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
        self.board = Board(self.boardFrame)
        self.board.boardFrame = self.boardFrame
        self.boardFrame.pack(side=TOP, fill=BOTH, expand=True)
        self.refreshGui()

        # Define commands linked to the view buttons
        self.defineCardsActions()
        pub.subscribe(self.listener1, 'refreshGUITopic')

    # Listener for GUI refresh
    def listener1(self):
        print 'Function listener1 received:'
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
            child = frames[index].winfo_children()[-1]
            command = partial(self.board.moveCardFromWaste, (index +1).__str__())
            child.configure(command=command)

    def defineTableauButtonActions(self):
        for key in self.boardFrame.cardButtons.keys():
            button  = self.boardFrame.cardButtons[key]
            command = partial(self.moveCardFromTableau, key)
            button.configure(command=command)

    def moveCardFromTableau(self, card):
        print("Moving " + card.__str__() + " from tableau")
        commandH = partial(self.board.moveCardFromTableau, card, "H")
        commandC = partial(self.board.moveCardFromTableau, card, "C")
        commandS = partial(self.board.moveCardFromTableau, card, "S")
        commandD = partial(self.board.moveCardFromTableau, card, "D")

        self.boardFrame.HButton.configure(command=commandH)
        self.boardFrame.CButton.configure(command=commandC)
        self.boardFrame.SButton.configure(command=commandS)
        self.boardFrame.DButton.configure(command=commandD)

        # frames = self.boardFrame.tableauFrames
        # for button in self.boardFrame.cardButtons.values():
            # command = partial(self.board.moveCardFromWaste, (index +1).__str__())
            # child.configure(command=command)
