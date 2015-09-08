from PIL import Image, ImageTk
from Tkinter import Frame, Button

class BoardFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.configure(background="#336600")

        # Divide screen in horizontal zones
        self.topFrame     = Frame(self)
        self.bottomFrame  = Frame(self)
        self.topFrame.pack(side="top", fill="x", expand=False)
        # self.bottomFrame.pack(side="bottom", fill="both", expand=True)
        self.bottomFrame.pack(side="bottom", fill="x", expand=True)

        # Divide the top frame in 2 vertically
        self.topLeft   = Frame(self.topFrame)
        self.topRight  = Frame(self.topFrame)
        self.topLeft.pack(side="left", fill="x", expand=True)
        self.topRight.pack(side="right", fill="x", expand=True)

        # In top left put 2 frames for the stock and the waste
        self.stockFrame = Frame(self.topLeft)
        self.wasteFrame = Frame(self.topLeft)
        self.stockFrame.pack(side="left", fill="x", expand=True)
        self.wasteFrame.pack(side="right", fill="x", expand=True)

        # In top right put 4 frames for the 4 foundations
        self.HFrame = Frame(self.topRight, background="yellow")
        self.CFrame = Frame(self.topRight, background="orange")
        self.SFrame = Frame(self.topRight, background="green")
        self.DFrame = Frame(self.topRight, background="grey")
        self.HFrame.pack(side="right", fill="both", expand=True)
        self.CFrame.pack(side="right", fill="both", expand=True)
        self.SFrame.pack(side="right", fill="both", expand=True)
        self.DFrame.pack(side="right", fill="both", expand=True)

        # Load common images
        self.photoBack    = ImageTk.PhotoImage(Image.open("../img/back.bmp"))
        self.photoEmpty   = ImageTk.PhotoImage(Image.open("../img/empty.bmp"))
        self.photoHEmpty  = ImageTk.PhotoImage(Image.open("../img/Hempty.bmp"))
        self.photoCEmpty  = ImageTk.PhotoImage(Image.open("../img/Cempty.bmp"))
        self.photoSEmpty  = ImageTk.PhotoImage(Image.open("../img/Sempty.bmp"))
        self.photoDEmpty  = ImageTk.PhotoImage(Image.open("../img/Dempty.bmp"))

        # Put initial waste button
        self.wasteButton = Button(self.wasteFrame, image=self.photoEmpty)
        self.wasteButton.photo = self.photoEmpty
        self.wasteButton.pack(side="top", fill="both", expand=False)

        # Put initial stock button
        self.stockButton = Button(self.stockFrame, image=self.photoBack)
        self.stockButton.photo = self.photoBack
        self.stockButton.pack(side="top", fill="both", expand=False)

        # Put initial foundations buttons
        self.HButton = Button(self.HFrame, image=self.photoHEmpty)
        self.CButton = Button(self.CFrame, image=self.photoCEmpty)
        self.SButton = Button(self.SFrame, image=self.photoSEmpty)
        self.DButton = Button(self.DFrame, image=self.photoDEmpty)
        self.HButton.pack(side="top", fill="both", expand=False)
        self.CButton.pack(side="top", fill="both", expand=False)
        self.SButton.pack(side="top", fill="both", expand=False)
        self.DButton.pack(side="top", fill="both", expand=False)


    # To be called by the board class when graphics are updated
    def updateGUI(self, board):
        print(board.__str__())

        # Update stock and waste buttons
        self.stockButton.configure(command=board.pickCardFromStock)
        resetStockButtonImage = True
        if (len(board.stock) > 0):
            self.wasteButton.configure(image=board.stock[-1].photoFaceUp)
            if (resetStockButtonImage):
                self.stockButton.configure(image=self.photoBack)
                resetStockButtonImage = False
        else:
            self.stockButton.configure(image=self.photoEmpty)
            resetStockButtonImage = True

        # Update foundations buttons
        if (len(board.H) > 0):
            self.HButton.configure(image=board.H[-1].photoFaceUp)
        if (len(board.C) > 0):
            self.CButton.configure(image=board.C[-1].photoFaceUp)
        if (len(board.S) > 0):
            self.SButton.configure(image=board.S[-1].photoFaceUp)
        if (len(board.D) > 0):
            self.DButton.configure(image=board.D[-1].photoFaceUp)
