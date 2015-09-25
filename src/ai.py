from card import Card
from board import Board

class AI():

    # Check for possible move given the state of the board
    def possibleMoves(self, board):

        return

    # Define if all the cards are discovered and placed in a way which
    # will always let the player finish the game
    def willWin(self, board):
        print("test victoire:")
        # Check if there is still some card in the board or in the waste
        if (len(board.stock) != 0 or len(board.waste)!=0):
            print ("cartes dans le stock ou dans le waste")
            return False

        # Check if some card on the tableau are still face down
        for pile in board.PlayingStacks:
            for card in pile:
                if (card.facedown):
                    print("Carte retournee")
                    return False

        print("victoire")
        return True
