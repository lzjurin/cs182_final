import chess
import os, sys

class Game(object):
    def __init__(self, config=None):
        if not config:
            self.game = chess.Board()
        else:
            self.game = chess.Board(fen=config)
        self.squares = chess.SQUARES
        self.WLesserValue = {1: [],2:[chess.Piece.from_symbol('p')],\
        3:[chess.Piece.from_symbol('p')],4:[chess.Piece.from_symbol('p'),chess.Piece.from_symbol('b'),chess.Piece.from_symbol('n')],\
        5: [chess.Piece.from_symbol('p'),chess.Piece.from_symbol('b'),chess.Piece.from_symbol('n'),chess.Piece.from_symbol('r')],\
        6: [chess.Piece.from_symbol('p'),chess.Piece.from_symbol('b'),chess.Piece.from_symbol('n'),chess.Piece.from_symbol('r'),chess.Piece.from_symbol('q')]}
        self.BLesserValue = {1: [],2:[chess.Piece.from_symbol('P')],\
        3:[chess.Piece.from_symbol('P')],4:[chess.Piece.from_symbol('P'),chess.Piece.from_symbol('B'),chess.Piece.from_symbol('N')],\
        5: [chess.Piece.from_symbol('P'),chess.Piece.from_symbol('B'),chess.Piece.from_symbol('N'),chess.Piece.from_symbol('R')],\
        6: [chess.Piece.from_symbol('P'),chess.Piece.from_symbol('B'),chess.Piece.from_symbol('N'),chess.Piece.from_symbol('R'),chess.Piece.from_symbol('Q')]}
        self.values = {1:1,2:3,3:3,4:5,5:9,6:1000}


    def move(self, move):
        try:
            self.game.push(move)
        except Exception as e:
            print e

    def move_san(self, move):
        try:
            self.game.push_san(move)
        except ValueError as e:
            print e

    def undo(self):
        try:
            self.game.pop()
        except Exception as e:
            print e

    def legalMoves(self, start=None):
        if not start:
            return [move for move in self.game.legal_moves]
        else:
            return [move for move in self.game.legal_moves if move.from_square == (start[0] * 8 + start[1])]

    def kingzone(self, color=True):
        position = list(self.game.pieces(6, color))[0]
        coords = [position / 8, position % 8]
        possibles = map(lambda i: map(lambda j: [coords[0] + i, coords[1] + j], xrange(-2, 3)), xrange(-2, 3))
        possibles = [pos for pos in possibles if (pos[0] * 8 + pos[1]) > -1 and (pos[0] * 8 + pos[1]) < 64]
        return possibles

    def turn(self):
        return "White" if self.game.turn else "Black"

    def turn_bool(self):
        return self.game.turn

    def getPositions(self):
        return [row.split() for row in self.game.__str__().split('\n')]

    def over(self):
        return self.game.is_game_over()
    def isDraw(self):
        return self.game.can_claim_threefold_repetition() or self.game.is_fivefold_repetition()

    def __str__(self):
        return self.game.__str__()

    def threatened(self):
        white = [[map(lambda pos: ((pos / 8, pos % 8), self.game.piece_at(pos)), list(self.game.attackers(True, row * 8 + col))) for col in range(8)] for row in range(8)]
        black = [[map(lambda pos: ((pos / 8, pos % 8), self.game.piece_at(pos)), list(self.game.attackers(False, row * 8 + col))) for col in range(8)] for row in range(8)]
        return (white, black)

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
