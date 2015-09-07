import os
import sys
from board import Board
from card import Card

board = Board()
print(board)

while True:
    print("=======================================")
    print("\t1. Pick card from stock")
    print("\t2. Pick card from waste")
    print("\t3. Pick card from tableau")
    print("\t99. Quit")
    print("\n")

    choice = raw_input("What to do?")

    if (choice == "1"):
        board.pickCardFromStock()
    elif (choice == "2"):
        destination = raw_input("Where do you want to put the card? (H/C/S/D/1-7)")
        board.moveCardFromWaste(destination)
    elif (choice == "3"):
        print("select a card")
        card = Card(raw_input("Symbole (H/S/C/D):"), raw_input("value (1-10/J/Q/K)"))
        destination = raw_input("Where do you want to put the card? (H/C/S/D/1-7)")
        board.moveCardFromTableau(card, destination)
    elif (choice == "99"):
        break
    else:
        print("Incorrect choice")

    print(board)
