from board import Board
from card import Card

class Game():

    def __init__(self):
        self.board = Board()
        print(self.board)

    def play(self):
        while True:
            print("=======================================")
            print("\t1. Pick card from stock")
            print("\t2. Pick card from waste")
            print("\t3. Pick card from tableau")
            print("\t4. Pick card from foundation")
            print("\t99. Quit")
            print("\n")

            choice = raw_input("What to do?")

            if (choice == "1"):
                self.board.pickCardFromStock()
            elif (choice == "2"):
                destination = raw_input("Where do you want to put the card? (H/C/S/D/1-7) :")
                self.board.moveCardFromWaste(destination)
            elif (choice == "3"):
                print("select a card")
                value  = raw_input("value (1-10/J/Q/K) :")
                symbol = raw_input("Symbole (H/S/C/D)  :") 
                card = Card(symbol, value)
                destination = raw_input("Where do you want to put the card? (H/C/S/D/1-7) :")
                self.board.moveCardFromTableau(card, destination)
            elif (choice == "4"):
                foundation  = raw_input("select a color (H/S/C/D) :")
                destination = raw_input("Where do you want to put the card? (1-7) :")
                self.board.moveCardFromFoundation(foundation, destination)
            elif (choice == "99"):
                break
            else:
                print("Incorrect choice")

            print(self.board)

