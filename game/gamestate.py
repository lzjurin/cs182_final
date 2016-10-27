import sys, math, itertools
from pieces import *

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
        self.log = []

    # When printing the game state, your pieces are uppercase and the opponent's are lowercase
    def __str__(self):
        out = '\n   A B C D E F G H \n'
        for rownum in range(8):
            out += str(rownum + 1) + ' |' + '|'.join([piece.charRep() if piece else ' ' for piece in self.board[rownum] ]) + '|\n'
        return out

    def move(self, start, end):
        print start, end
        if not (self.onBoard(start) and self.onBoard(end)):
            print "That move doesn't start/end on the board."
            return False
        piece = self.positions[start]
        if not piece:
            print "No piece at that starting position."
            return False

        print piece
        print piece.moves()

        if piece.player != self.player:
            print piece.player
            print "You can't move a piece that's not yours!"
            return False

        possibleMoves = [move for move in piece.moves() if self.onBoard(move)]
        if not end in possibleMoves:
            print "The piece at position {0} cannot move to position {1}".format(start, end)
            return False

        if piece.linear:
            between = zip(range(start[0], end[0]), range(start[1], end[1]))
            if between[1:]:
                for el in between[1:]:
                    if self.positions[el]:
                        print "The piece at position {0} is blocked from moving to position {1}".format(start, end)
                        return False

        piece.setPosition(end)
        del self.positions[start]
        if end in self.positions.keys():
            if self.positions[end].player == self.player:
                print "Cannot take your own piece!"
                return False
            self.config.pieces.remove(self.positions[end])
        self.positions[end] = piece
        self.board[start[0]][start[1]] = None
        self.board[end[0]][end[1]] = piece
        print self.board[end[0]][end[1]]

        return True


    def onBoard(self, pos):
        return -1 < pos[0] < 8 and -1 < pos[1] < 8
