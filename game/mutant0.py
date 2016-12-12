import chess, game
import os, sys
import eval
g = game.Game(config='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
e = eval.ChessAI(g, params=[0.025430824182692987, 0.028407460981331067, 0.012570971348237129, 0.012588494512726823, 0.005948991527664038, 0.035004389456069575, 0.005480314496200913, 0.017485269544117495])
moves = 0
while moves < 10 and not g.over() and not g.isDraw():
	moves += 1
	score, move = e.nextMove()
	g.move(move)
	print g
print e.eval()
