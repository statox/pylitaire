#!/usr/bin/python2
import os
import sys 
from game import Game
from board import Board
from boardFrame import BoardFrame
from Tkinter import *

class MainApp:
    def __init__(self, master):
        # self.frame = Frame(master, background="#336600")
        # self.frame = BoardFrame(master)

        self.board = Board(master)
        self.boardFrame = self.board.boardFrame
        self.boardFrame.pack(side=TOP, fill=BOTH, expand=True)
        

    # def pickCardFromStock(self):
        # print(self.board)
        # self.board.pickCardFromStock()
        # print(self.board)

    # def getWasteButtonText(self):
        # if (len(self.board.waste) > 0):
            # str = self.board.waste[-1].__str__()
        # else:
            # str = "##"
        # self.wasteButton.text = str
        # self.wasteButton.update()

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
app = MainApp(root)
root.mainloop()

# game = Game()
# game.play()
