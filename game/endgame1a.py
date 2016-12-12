import chess, game
import os, sys
import eval
from subprocess import call
import copy
import numpy as np

# Initialize initial game with aggressive strategy
g = game.Game(config='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
curParams = [0.025,0.25,0.0125,0.0125,0.0067,0.033,0.005,0.02]
moves = 0

while moves < 10 or not g.over() or not g.isDraw():
	moves += 1
	allMuts = []
	for i in range(5):
		mutParams = []
		for i in range(len(curParams)):
			value = curParams[i] * np.random.uniform(1 - np.random.random()*2 / float(moves), 1 + np.random.random()*2 / float(moves))
			if i == 1:
				while value < 0.1:
					value = curParams[i] * np.random.uniform(1 - np.random.random()*2 / float(moves), 1 + np.random.random()*2 / float(moves))
			mutParams.append()
		allMuts.append(mutParams)
		f1 = open('mutant' + str(i) + '.py', 'w')
		f1.write('import chess, game')
		f1.write('import os, sys')
		f1.write('import eval')
		f1.write('g = game.Game(config=\'' + g.game.fen() + '\')')
		f1.write('e = eval.ChessAI(g, params=' + str(mutParams) + ')')
		f1.write('for _ in range(10):')
		f1.write('\tscore, move = e.nextMove()')
		f1.write('\tg.move(move)')
		f1.write('print e.eval()')
		f2 = open('mutant' + str(i) + '.sh', 'w')
		f2.write('#!/bin/bash')
		f2.write('#SBATCH -t 60')
		f2.write('#SBATCH -p serial_requeue')
		f2.write('#SBATCH -N 1')
		f2.write('#SBATCH -c 4')
		f2.write('#SBATCH --mem=32000')
		f2.write('#SBATCH -o mutant' + str(i) + '.out')
		f2.write('#SBATCH -e mutant' + str(i) + '.err')
		f2.write('#SBATCH --mail-type=END')
		f2.write('#SBATCH --mail-user=benjaminzheng@college.harvard.edu')
		f2.write('python mutant' + str(i) + '.py')

		f1.close()
		f2.close()

		call(["sbatch", "mutant" + str(i) + ".sh"])

	best = 99999999999.0
	for i in range(5):
		done = False
		while not done:
			if os.path.exists('mutant' + str(i) + '.out') and os.path.getsize('mutant' + str(i) + '.out') > 0:
				done = True
		f3 = open('mutant' + str(i) + '.out', 'r')
		# Parse and find best score
		result = float(f3.readline())
		f3.close()
		if result < best:
			best = result
			curParams = allMuts[i]

	standard = eval.ChessAI(g, params=curParams)
	score, move = standard.nextMove()
	g.move(move)
	print("Move #" + str(moves) + ":")
	print("Move: " + str(move))
	print("Score: " + str(score))
	print("Params: " + str(curParams))