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
        self.stockFrame = Frame(self.topLeft)
        self.wasteFrame = Frame(self.topLeft)
        self.stockFrame.pack(side="left", fill="x", expand=True)
        self.wasteFrame.pack(side="right", fill="x", expand=True)

        # In top right put 4 frames for the 4 foundations
        self.HFrame = Frame(self.topRight)
        self.CFrame = Frame(self.topRight)
        self.SFrame = Frame(self.topRight)
        self.DFrame = Frame(self.topRight)
        self.HFrame.pack(side="right", fill="both", expand=True)
        self.CFrame.pack(side="right", fill="both", expand=True)
        self.DFrame.pack(side="right", fill="both", expand=True)
        self.SFrame.pack(side="right", fill="both", expand=True)

        # In bottom frame put 7 frames for the tableau piles
        self.tableauFrames = []
        for i in range(0, 7):
            self.tableauFrames.append(Frame(self.bottomFrame))
            self.tableauFrames[i].pack(side="left", fill="y", expand=True)

        # Dictionary which will links cards in the tableau
        # to buttons which represent them
        self.cardButtons = {}

        # When a tableau pile is empty, a corresponding button will be stored
        # in this dictionnary to allow the user to put a card on an empty pile
        self.tableauFirstCardButtons = {}

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



    # To be called by the controller when the board 
    # publish the refreshGUI event
    def updateGUI(self, board):
        print(board.__str__())

        # Update stock and waste buttons
        resetStockButtonImage = True
        if (len(board.stock) > 0):
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
        
        # Remove old buttons in each frame
        for f in self.tableauFrames:
            if (len(f.winfo_children()) > 0):
                for child in f.winfo_children():
                    child.destroy()

        frame = -1
        for pile in board.PlayingStacks:
            frame += 1
            r = -1

            # if a pile is empty, create a button to represent it and add 
            # the button to the dictionary.
            # If the pile is not empty anymore destroy the button.
            if (len(pile) == 0):
                newButton = Button(self.tableauFrames[frame], image=self.photoEmpty)
                newButton.grid(row=0, column=0)
                self.tableauFirstCardButtons[frame] = newButton
            elif frame in self.tableauFirstCardButtons:
                self.tableauFirstCardButtons[frame].destroy()
                del self.tableauFirstCardButtons[frame]

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

                newButton = Button(self.tableauFrames[frame], image=image)
                newButton.grid(row=r, column=0)
                if (not card.facedown):
                    self.cardButtons[card] = newButton

        # remove old entries from dictionary
        for k in self.cardButtons.keys():
            isInTableau = False
            for stack in board.PlayingStacks:
                if k in stack:
                    isInTableau = True
                    break
            if (not isInTableau):
                self.cardButtons.pop(k, None)
