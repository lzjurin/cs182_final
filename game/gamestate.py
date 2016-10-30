import sys, math, itertools
from pieces import *

# Invalid move exception class, meant to propogate errors to the main app to be logged
class InvalidMoveException(Exception):
    def __init__(self, move, err):
        self.move = move
        self.err = err

    def __str__(self):
        return "Move from {0} to {1} is invalid: {2}".format(move[0], move[1], err)

# Config class. Meant only to keep track of pieces still on the board and their positions.
class GameConfig(object):
    def __init__(self, pieces=None):
        self.pieces = pieces if pieces else self.default()

    def default(self):
        return ([
            Rook(0, 0, player="Black"),
            Knight(0, 1, player="Black"),
            Bishop(0, 2, player="Black"),
            Queen(0, 3, player="Black"),
            King(0, 4, player="Black"),
            Bishop(0, 5, player="Black"),
            Knight(0, 6, player="Black"),
            Rook(0, 7, player="Black") ] +
        [Pawn(6, i) for i in range(8)] +
        [Pawn(1, i, player="Black") for i in range(8)] +
        [Rook(7, 0), Knight(7, 1), Bishop(7, 2), Queen(7, 3), King(7, 4), Bishop(7, 5), Knight(7, 6), Rook(7, 7)])

# Game state. Augments configuration with turn tracker and various statistics
class GameState(object):

    def __init__(self, config=GameConfig(), player="White"):
        self.config = config
        self.player = player
        self.positions = dict([ (piece.getPos(), piece) for piece in self.config.pieces ])
        self.board = [ [self.positions[i, j] if (i, j) in self.positions else None for j in range(8)] for i in range(8) ]
        self.lastmove = None

    # When printing the game state, your pieces are uppercase and the opponent's are lowercase
    def __str__(self):
        out = '\n   A B C D E F G H \n'
        for rownum in range(8):
            out += str(rownum + 1) + ' |' + '|'.join([piece.charRep() if piece else ' ' for piece in self.board[rownum] ]) + '|\n'
        return out

    def move(self, start, end):
        # Ensure both moves are on the board
        if not (self.onBoard(start) and self.onBoard(end)):
            raise InvalidMoveException((start, end), "doesn't start/end on the board.")

        # Ensure there's a piece at the starting position
        piece = self.positions[start]
        if not piece:
            raise InvalidMoveException((start, end), "no piece at starting position")

        # Ensure the piece is yours
        if piece.player != self.player:
            raise InvalidMoveException((start, end), "piece does not belong to player")

        # If the current piece is a Pawn, could take a piece diagonally
        endpiece = None
        if piece.getClass() == 'Pawn':
            # Check for end being diagonally ahead and ensure that there's an enemy piece there
            moveOne = piece.moves()[0]
            if end in ((moveOne[0], moveOne[1] - 1), (moveOne[0], moveOne[1] + 1)):
                if end in self.positions:
                    if self.positions[end].player == self.player:
                        raise InvalidMoveException((start, end), "Cannot take your own piece!")
                    endpiece = self.positions[end]
                    self.config.pieces.remove(self.positions[end])


        # Get list of possible moves and ensure move is possible and isn't blocked
        possibleMoves = [move for move in piece.moves() if self.onBoard(move)]
        if not end in possibleMoves:
            raise InvalidMoveException((start, end), "piece cannot move in that manner")

        if piece.linear:
            between = zip(range(start[0], end[0]), range(start[1], end[1]))
            if between[1:]:
                for el in between[1:]:
                    if self.positions[el]:
                        raise InvalidMoveException((start, end), "piece movement is blocked in that direction")

        # Check that the end position isn't one of the player's own pieces
        if end in self.positions:
            if self.positions[end].player == self.player:
                raise InvalidMoveException((start, end), "Cannot take your own piece!")

            # Delete the other player's piece
            endpiece = self.positions[end]
            self.config.pieces.remove(self.positions[end])

        # Move the piece and update tracked positions
        piece.setPosition(end)
        startpiece = piece
        del self.positions[start]
        self.positions[end] = piece

        # Update board positions
        self.board[start[0]][start[1]] = None
        self.board[end[0]][end[1]] = piece

        # Update last move
        self.lastmove = (startpiece, endpiece, start, end)

        # Return success
        return True

    def onBoard(self, pos):
        return -1 < pos[0] < 8 and -1 < pos[1] < 8
