import chess
import os, sys

class Game(object):
    def __init__(self):
        self.game = chess.Board()
        self.squares = chess.SQUARES

    def move(self, move):
        try:
            self.game.push_san(move)
        except ValueError as e:
            print e

    def legalMoves(self):
        return [str(move) for move in self.game.legal_moves]

    def turn(self):
        return "White" if self.game.turn else "Black"

    def getPositions(self):
        return [row.split() for row in self.game.__str__().split('\n')]

    def over(self):
        return self.game.is_game_over()

    def __str__(self):
        return self.game.__str__()

    def threatened(self):
        white = [[map(self.game.piece_at, list(self.game.attackers(True, row * 8 + col))) for col in range(8)] for row in range(8)]
        black = [[map(self.game.piece_at, list(self.game.attackers(False, row * 8 + col))) for col in range(8)] for row in range(8)]
        return (white, black)

    def available(self):
        legal = [move for move in self.game.legal_moves]
        legalsquares = {}
        for move in legal:
            if not move.to_square in legalsquares:
                legalsquares[move.to_square] = [self.game.piece_at(move.from_square)]
            else:
                legalsquares[move.to_square].append(self.game.piece_at(move.from_square))

        self.game.turn = not self.game.turn

        otherlegal = [move for move in self.game.legal_moves]
        otherlegalsquares = {}
        for move in otherlegal:
            if not move.to_square in otherlegalsquares:
                otherlegalsquares[move.to_square] = [self.game.piece_at(move.from_square)]
            else:
                otherlegalsquares[move.to_square].append(self.game.piece_at(move.from_square))

        self.game.turn = not self.game.turn

        return (legalsquares, otherlegalsquares) if self.game.turn else (otherlegalsquares, legalsquares)

    # True = white, False = black
    # 1 = pawn, 2 = knight, 3 = bishop, 4 = rook, 5 = queen, 6 = king
    def pieces(self, color=True, piece_type=1):
        return map(lambda index: (index / 8, index % 8), list(self.game.pieces(piece_type, color)))
