from functools import partial
from boardFrame import BoardFrame
from board import Board
from Tkinter import *

class BoardController:
    def __init__(self):
        self.root = Tk()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))

        self.board = Board(self.root)
        self.boardFrame = self.board.boardFrame
        self.boardFrame.pack(side=TOP, fill=BOTH, expand=True)

        # Define commands linked to the view buttons
        self.boardFrame.stockButton.configure(command=self.pickCardFromStock)
        self.boardFrame.wasteButton.configure(command=self.moveCardFromWaste)



    def startGame(self):
        self.root.mainloop()

    def pickCardFromStock(self):
        self.board.pickCardFromStock()

    def moveCardFromWaste(self):
        self.boardFrame.HButton.configure(command=lambda: self.board.moveCardFromWaste("H") )
        self.boardFrame.CButton.configure(command=lambda: self.board.moveCardFromWaste("C") )
        self.boardFrame.SButton.configure(command=lambda: self.board.moveCardFromWaste("S") )
        self.boardFrame.DButton.configure(command=lambda: self.board.moveCardFromWaste("D") )

        frames = self.boardFrame.tableauFrames
        for index in range (0, 7):
            child = frames[index].winfo_children()[-1]
            command = partial(self.board.moveCardFromWaste, (index +1).__str__())
            child.configure(command=command)
