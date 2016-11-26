from game.game import *
import chess
import os, sys

tests = os.listdir('tests/')
for test in tests:
    moves = [line.strip() for line in open('tests/{0}'.format(test)).readlines()]
    game = chess.Board()
    for move in moves:
        try:
            game.push_san(move)
        except ValueError as e:
            print e
