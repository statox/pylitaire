from card import Card
from board import Board

class AI():

    # Check for possible move given the state of the board
    def possibleMoves(self, board):
        # List of the possible moves
        # a move is a tuple (cardOrigin, cardDestination)
        moves = []

        # Test cards of the tableau
        for pile in board.PlayingStacks:
            for card in pile:
                if (not card.facedown):
                    # Moves on the tableau
                    for pile2 in board.PlayingStacks:
                        if (pile != pile2):
                            for card2 in pile2:
                                if (board.moveCardFromTableau(card, card2) == 0):
                                    moves.append([card, card2])
                    # Moves on the foundations
                    if (board.moveCardFromTableau(card, "H") == 0):
                        moves.append([card, "H"])
                    if (board.moveCardFromTableau(card, "S") == 0):
                        moves.append([card, "S"])
                    if (board.moveCardFromTableau(card, "C") == 0):
                        moves.append([card, "C"])
                    if (board.moveCardFromTableau(card, "D") == 0):
                        moves.append([card, "D"])

        # Test card of the waste
        if (len(board.waste) > 0):
            # Move to the tableau
            for pile in board.PlayingStacks:
                if (len(pile) > 0):
                    destinationCard = pile[-1]
                    if (board.moveCardFromWaste(destinationCard) == 0):
                        moves.append([ board.waste[-1], destinationCard ])

            # Moves on the foundations
            if (board.moveCardFromWaste("H") == 0):
                moves.append([board.waste[-1], "H"])
            if (board.moveCardFromWaste("S") == 0):
                moves.append([board.waste[-1], "S"])
            if (board.moveCardFromWaste("C") == 0):
                moves.append([board.waste[-1], "C"])
            if (board.moveCardFromWaste("D") == 0):
                moves.append([board.waste[-1], "D"])

        # If not move is possible from the waste or from the tableau
        # search for moves from the foundattions
        # Test card from the foundations
        if (not moves):
            if (len(board.H) > 0):
                # Move to the tableau
                for pile in board.PlayingStacks:
                    if (len(pile) > 0):
                        destinationCard = pile[-1]
                        if (board.moveCardFromFoundation("H", destinationCard) == 0):
                            moves.append([ board.H[-1], destinationCard ])

            if (len(board.S) > 0):
                # Move to the tableau
                for pile in board.PlayingStacks:
                    if (len(pile) > 0):
                        destinationCard = pile[-1]
                        if (board.moveCardFromFoundation("S", destinationCard) == 0):
                            moves.append([ board.S[-1], destinationCard ])

            if (len(board.C) > 0):
                # Move to the tableau
                for pile in board.PlayingStacks:
                    if (len(pile) > 0):
                        destinationCard = pile[-1]
                        if (board.moveCardFromFoundation("C", destinationCard) == 0):
                            moves.append([ board.C[-1], destinationCard ])

            if (len(board.D) > 0):
                # Move to the tableau
                for pile in board.PlayingStacks:
                    if (len(pile) > 0):
                        destinationCard = pile[-1]
                        if (board.moveCardFromFoundation("D", destinationCard) == 0):
                            moves.append([ board.D[-1], destinationCard ])



        return moves



    # Define if all the cards are discovered and placed in a way which
    # will always let the player finish the game
    def willWin(self, board):
        # Check if there is still some card in the board or in the waste
        if (len(board.stock) != 0 or len(board.waste)!=0):
            return False

        # Check if some card on the tableau are still face down
        for pile in board.PlayingStacks:
            for card in pile:
                if (card.facedown):
                    return False

        return True
