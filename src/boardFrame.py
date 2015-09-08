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
        self.bottomFrame.pack(side="top", fill="both", expand=True)

        # Divide the top frame in 2 vertically
        self.topLeft   = Frame(self.topFrame)
        self.topRight  = Frame(self.topFrame)
        self.topLeft.pack(side="left", fill="x", expand=True)
        self.topRight.pack(side="right", fill="x", expand=True)

        # In top left put 2 frames for the stock and the waste
        self.stockFrame = Frame(self.topLeft, background="#336600")
        self.wasteFrame = Frame(self.topLeft, background="#336600")
        self.stockFrame.pack(side="left", fill="x", expand=True)
        self.wasteFrame.pack(side="right", fill="x", expand=True)

        # In top right put 4 frames for the 4 foundations
        self.HFrame = Frame(self.topRight, background="#336600")
        self.CFrame = Frame(self.topRight, background="#336600")
        self.SFrame = Frame(self.topRight, background="#336600")
        self.DFrame = Frame(self.topRight, background="#336600")
        self.HFrame.pack(side="right", fill="both", expand=True)
        self.CFrame.pack(side="right", fill="both", expand=True)
        self.SFrame.pack(side="right", fill="both", expand=True)
        self.DFrame.pack(side="right", fill="both", expand=True)

        # In bottom frame put 7 frames for the tableau piles
        self.tableauFrames = []
        for i in range(0, 7):
            self.tableauFrames.append(Frame(self.bottomFrame, background="#336600"))
            self.tableauFrames[i].pack(side="left", fill="y", expand=True)

        # Load common images
        imageBack              = Image.open("../img/back.bmp")
        self.photoBack         = ImageTk.PhotoImage(imageBack)
        self.photoBackCropped  = ImageTk.PhotoImage(imageBack.crop((0, 0, imageBack.size[0], imageBack.size[1]/4)))
        self.photoEmpty        = ImageTk.PhotoImage(Image.open("../img/empty.bmp"))
        self.photoHEmpty       = ImageTk.PhotoImage(Image.open("../img/Hempty.bmp"))
        self.photoCEmpty       = ImageTk.PhotoImage(Image.open("../img/Cempty.bmp"))
        self.photoSEmpty       = ImageTk.PhotoImage(Image.open("../img/Sempty.bmp"))
        self.photoDEmpty       = ImageTk.PhotoImage(Image.open("../img/Dempty.bmp"))

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
        resetStockButtonImage = True
        if (len(board.stock) > 0):
            # self.wasteButton.configure(image=board.stock[-1].photoFaceUp)
            # self.wasteButton.configure(image=board.waste[-1].photoFaceUp)
            if (resetStockButtonImage):
                self.stockButton.configure(image=self.photoBack)
                resetStockButtonImage = False
        else:
            self.stockButton.configure(image=self.photoEmpty)
            resetStockButtonImage = True

        if (len(board.waste) == 0):
            self.wasteButton.configure(image=self.photoEmpty)
        else:
            self.wasteButton.configure(image=board.waste[-1].photoFaceUp)

        # Update foundations buttons
        if (len(board.H) > 0):
            self.HButton.configure(image=board.H[-1].photoFaceUp)
        if (len(board.C) > 0):
            self.CButton.configure(image=board.C[-1].photoFaceUp)
        if (len(board.S) > 0):
            self.SButton.configure(image=board.S[-1].photoFaceUp)
        if (len(board.D) > 0):
            self.DButton.configure(image=board.D[-1].photoFaceUp)

        # Update tableau piles
        frame = -1
        for pile in board.PlayingStacks:
            frame += 1
            r = -1
            for card in pile:
                r += 1

                if (card != pile[-1]):
                    if (card.facedown):
                        image=self.photoBackCropped
                    else:
                        image=card.photoFaceUpCropped
                else:
                    if (card.facedown):
                        image=self.photoBack
                    else:
                        image=card.photoFaceUp


                Button(self.tableauFrames[frame], image=image).grid(row=r, column=0)
