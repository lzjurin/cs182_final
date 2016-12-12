import chess, game
import os, sys
import eval
g = game.Game(config='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
e = eval.ChessAI(g, params=[0.024562342593483125, 0.027540094386543985, 0.0131791247140367, 0.012289693586295976, 0.006638471293781575, 0.03291191639520942, 0.005010119068196424, 0.018153570581693514])
moves = 0
while moves < 10 and not g.over() and not g.isDraw():
	moves += 1
	score, move = e.nextMove()
	g.move(move)
print e.eval()