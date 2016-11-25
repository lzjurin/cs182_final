import sys, math, itertools
from pieces import *

# Invalid move exception class, propogates errors up to the main app to be logged
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
        [Pawn(1, i, player="Black") for i in range(8)] +
        [Pawn(6, i) for i in range(8)] +
        [Rook(7, 0), Knight(7, 1), Bishop(7, 2), Queen(7, 3), King(7, 4), Bishop(7, 5), Knight(7, 6), Rook(7, 7)])

# Game state. Actually runs the game. Takes a configuration and a starting player, has move tracker, current player, etc.
class GameState(object):

    def __init__(self, config=GameConfig(), player="White"):
        # Store starting game configuration, current player, pieces' positions, the board state, and a move history
        self.config = config
        self.player = player
        self.startPositions = dict([ (piece.getPos(), piece) for piece in self.config.pieces ])
        self.board = [ [self.positions[i, j] if (i, j) in self.positions else None for j in range(8)] for i in range(8) ]
        self.moves = []

    # When printing the game state, White pieces are uppercase and Black pieces are lowercase, and game is oriented with Black on top and White on bottom
    def __str__(self):
        out = '\n   A B C D E F G H \n'
        for rownum in range(8):
            out += str(rownum + 1) + ' |' + '|'.join([piece.charRep() if piece else ' ' for piece in self.board[rownum] ]) + '|\n'
        return out

    def checkValidMove(self, player=self.player, start, end):
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

        # Get piece at end if any
        endpiece = self.positions[end]

        # Get list of possible moves and ensure move is possible and isn't blocked
        possibleMoves = [move for move in piece.moves() if self.onBoard(move)]
        if not end in possibleMoves:
            # If it's not in the standard list of possible moves, then it's a special move, i.e. Pawn capturing, moving two forward at the start, en passant, or castling
            # If the current piece is a Pawn, check specials
            if piece.getClass() == "Pawn":
                # Check for moving two forward at the beginning, i.e. no pieces within two forward and that we're still at the starting position
                if (piece.getPos()[0] % 5 == 1 and end[0] == 4 - (piece.getPos()[0] % 6) and end[1] == self.getPos()[1] and not (self.positions[end] or self.positions[(piece.getPos()[0] + (1 if self.player == "Black" else -1), piece.getPos()[1])])) or

                # Diagonal capture or en passant
                # Check for end being diagonally ahead and ensure that there's an piece there that is an enemy OR that we have an adjacent enemy pawn and are on the appropriate rows plus that the last move was by the enemy pawn moving two forward
                (end[0] - piece.getPos()[0] == (1 if piece.player == "Black" else -1) and abs(end[1] - piece.getPos()[1]) == 1 and ((self.positions[end].player and self.positions[end].player != piece.player) or (self.positions[(piece.getPos()[0], end[1])] and self.positions[(piece.getPos()[0], end[1])].player != piece.player and int(piece.player == "White") == piece.getPos()[0] % 3 and self.moves[-1][0] == self.positions[(piece.getPos()[0], end[1])] and self.moves[-1][2] % 5 == 1))):
                    return True


                # Check for en passant, i.e. adjacent to an enemy directly ahead of the end position, end position is equivalent to a diagonal capture and last move made was by the adjacent pawn and pieces are on the 3/4 line (depending on which side)

                     and end in self.positions :
                    if end in self.positions:
                        if self.positions[end].player == self.player:
                            raise InvalidMoveException((start, end), "Cannot take your own piece!")
                        endpiece = self.positions[end]
                        self.config.pieces.remove(self.positions[end])
                # Check for en passant
                elif self.lastmove[0].getClass() == "Pawn" and self.lastmove[0].getPlayer() != self.player and
                    self.lastmove[0]

            raise InvalidMoveException((start, end), "{0} cannot move in that manner".format(piece.getClass()))

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
