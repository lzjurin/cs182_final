import chess
import os, sys

class Game(object):
    def __init__(self):
        self.game = chess.Board()

    def move(self, move):
        try:
            self.game.push_san(move)
        except ValueError as e:
            print e

    def legalMoves(self):
        return [str(move) for move in self.game.legalmoves]

    def turn(self):
        return "White" if self.game.turn else "Black"

    def getPositions(self):
        return [row.split() for row in self.game.__str__().split('\n')]

    def over(self):
        return self.game.is_game_over()

    def __str__(self):
        return self.game.__str__()
