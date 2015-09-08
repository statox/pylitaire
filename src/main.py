#!/usr/bin/python2
import os
import sys 
from game import Game
from board import Board
from boardFrame import BoardFrame
from Tkinter import *

class MainApp:
    def __init__(self, master):
        self.board = Board(master)
        self.boardFrame = self.board.boardFrame
        self.boardFrame.pack(side=TOP, fill=BOTH, expand=True)

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
app = MainApp(root)
root.mainloop()
