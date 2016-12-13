import chess
import os, sys
from collections import deque

class Game(object):
    def __init__(self, config=None):

        # If a config is specified, set it up that way, otherwise start out default
        if not config:
            self.game = chess.Board()
        else:
            self.game = chess.Board(fen=config)

        # Get a list of squares
        self.squares = chess.SQUARES

        # Store dictionary of pieces of lesser value
        self.WLesserValue = {1: [],2:[chess.Piece.from_symbol('p')],\
        3:[chess.Piece.from_symbol('p')],4:[chess.Piece.from_symbol('p'),chess.Piece.from_symbol('b'),chess.Piece.from_symbol('n')],\
        5: [chess.Piece.from_symbol('p'),chess.Piece.from_symbol('b'),chess.Piece.from_symbol('n'),chess.Piece.from_symbol('r')],\
        6: [chess.Piece.from_symbol('p'),chess.Piece.from_symbol('b'),chess.Piece.from_symbol('n'),chess.Piece.from_symbol('r'),chess.Piece.from_symbol('q')]}
        self.BLesserValue = {1: [],2:[chess.Piece.from_symbol('P')],\
        3:[chess.Piece.from_symbol('P')],4:[chess.Piece.from_symbol('P'),chess.Piece.from_symbol('B'),chess.Piece.from_symbol('N')],\
        5: [chess.Piece.from_symbol('P'),chess.Piece.from_symbol('B'),chess.Piece.from_symbol('N'),chess.Piece.from_symbol('R')],\
        6: [chess.Piece.from_symbol('P'),chess.Piece.from_symbol('B'),chess.Piece.from_symbol('N'),chess.Piece.from_symbol('R'),chess.Piece.from_symbol('Q')]}

        # Store dictionary of piece type to values, and whether a side has castled
        self.values = {1:1,2:3,3:3,4:5,5:9,6:1000}
        self.castled = [False] * 2

    # Check if a given square is pinned by an enemy piece
    # Only counts as pinned if the enemy piece has lesser value than the pinned piece which in turn must have lesser value than the piece behind it
    # OR if both the pinned pieces are "free", i.e. not defended
    def pinned(self, square):

        # Find the piece at the square, if None then it can't be pinned
        piece = self.game.piece_at(square)
        if not piece:
            return False

        # Get all attackers and find each attacker's attacked squares
        attackers = list(self.game.attackers(not piece.color, square))
        attackedsquares = map(self.game.attacks, attackers)

        # Store old movestack for resetting when done checking pinning
        movestack = deque(map(lambda move: chess.Move.from_uci(move.uci()), list(self.game.move_stack)))

        # Remove the piece and get new attacked squares to look for hidden attacks, then put back the piece and movestack
        self.game.remove_piece_at(square)
        newsquares = map(self.game.attacks, attackers)
        self.game.set_piece_at(square, piece)
        self.game.move_stack = movestack

        # Iterate over each attacker and look for qualifying pins
        for i in xrange(len(attackers)):
            attacker = self.game.piece_at(attackers[i])
            for pos in newsquares[i]:
                if self.game.piece_at(pos) and pos not in attackedsquares[i] and self.game.piece_at(pos).piece_type > piece.piece_type and (self.game.piece_at(pos).piece_type > attacker.piece_type or not (self.defended(pos, piece.color) and self.defended(square, piece.color))):
                    return True
        return False

    # Check if a square is defended by a given player
    def defended(self, square, color=True):
        return any(self.game.attackers(color, square))

    # Check if a given square is being forked by an enemy piece
    def forked(self, square):

        # Find the piece at the square, if None then it can't be forked
        piece = self.game.piece_at(square)
        if not piece:
            return False

        # Get all attackers and find each attacker's attacked squares
        attackers = list(self.game.attackers(not piece.color, square))
        attackedsquares = map(self.game.attacks, attackers)

        # Iterate over attackers and look for qualifying forks
        for i in xrange(len(attackers)):
            attacker = self.game.piece_at(attackers[i])
            for attacked in attackedsquares[i]:
                if attacked != square and self.game.piece_at(attacked) and ((self.game.piece_at(attacked).piece_type > attacker.piece_type or not self.defended(attacked, piece.color)) or (piece.piece_type > attacker.piece_type or not self.defended(square, piece.color))):
                    return True
        return False

    # Make a move and record castling moves if one is made
    def move(self, move):
        try:
            if self.game.is_castling(move):
                self.hasCastled[int(self.turn)] = True
            self.game.push(move)
        except Exception as e:
            print e

    # Make a move passed in SAN format
    # DO NOT USE, NOT UPKEPT
    def move_san(self, move):
        try:
            self.game.push_san(move)
        except ValueError as e:
            print e

    # Undo previous move
    def undo(self):
        try:
            self.game.pop()
        except Exception as e:
            print e

    # Get a list of legal moves, with optional constraints of a starting square and a player
    def legalMoves(self, start=None, color=None):
        if not start:
            if not color:
                return [move for move in self.game.legal_moves]
            else:
                old = self.game.turn
                self.game.turn = color
                out = [move for move in self.game.legal_moves]
                self.game.turn = old
                return out
        else:
            return [move for move in self.game.legal_moves if move.from_square == (start[0] * 8 + start[1])]

    # Check whether a player has castled (defaults to White)
    def hasCastled(self, color=True):
        return self.castled[int(color)]

    # Gets a list of all the squares that comprise the kingzone given the current king position
    def kingzone(self, color=True):
        position = list(self.game.pieces(6, color))[0]
        coords = [position / 8, position % 8]
        possibles = map(lambda i: map(lambda j: [coords[0] + i, coords[1] + j], xrange(-2, 3)), xrange(-2, 3))
        possibles = [pos for pos in possibles if (pos[0] * 8 + pos[1]) > -1 and (pos[0] * 8 + pos[1]) < 64]
        return possibles

    # Get whose turn it is (both string and boolean formats)
    def turn(self):
        return "White" if self.game.turn else "Black"
    def turn_bool(self):
        return self.game.turn

    # Get a list of all the current positions of pieces on the board
    def getPositions(self):
        return [row.split() for row in self.game.__str__().split('\n')]

    # Is the game over? Is it a draw?
    def over(self):
        return self.game.is_game_over()

    def isDraw(self):
        return self.game.can_claim_threefold_repetition()

    # String representation - propagate up the str representation from the chessboard. This is a wrapper, after all, not a reimplementation. :P
    def __str__(self):
        return self.game.__str__()

    # Get a list of threatened squares
    def threatened(self):
        white = [[map(lambda pos: ((pos / 8, pos % 8), self.game.piece_at(pos)), list(self.game.attackers(True, row * 8 + col))) for col in range(8)] for row in range(8)]
        black = [[map(lambda pos: ((pos / 8, pos % 8), self.game.piece_at(pos)), list(self.game.attackers(False, row * 8 + col))) for col in range(8)] for row in range(8)]
        return (white, black)

    # Get a list of available squares on each side
    def available(self):
        legal = [move for move in self.game.legal_moves]
        legalsquares = {}
        for move in legal:
            piece = self.game.piece_at(move.from_square)
            tosquare_tup = (move.to_square / 8, move.to_square % 8)
            if not move.to_square in legalsquares:
                legalsquares[tosquare_tup] = [piece]
            else:
                legalsquares[tosquare_tup].append(piece)

        self.game.turn = not self.game.turn

        otherlegal = [move for move in self.game.legal_moves]
        otherlegalsquares = {}
        for move in otherlegal:
            piece = self.game.piece_at(move.from_square)
            tosquare_tup = (move.to_square / 8, move.to_square % 8)
            if not move.to_square in otherlegalsquares:
                otherlegalsquares[tosquare_tup] = [piece]
            else:
                otherlegalsquares[tosquare_tup].append(piece)

        self.game.turn = not self.game.turn

        return (legalsquares, otherlegalsquares) if self.game.turn else (otherlegalsquares, legalsquares)

    # True = white, False = black
    # 1 = pawn, 2 = knight, 3 = bishop, 4 = rook, 5 = queen, 6 = king
    def pieces(self, color=True, piece_type=1):
        return map(lambda index: (index / 8, index % 8), list(self.game.pieces(piece_type, color)))
