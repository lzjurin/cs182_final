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

while moves < 10 and not g.over() and not g.isDraw():
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
		f1 = open('mutant' + str(i) + 'a.py', 'w')
		f1.write('import chess, game\n')
		f1.write('import os, sys\n')
		f1.write('import eval\n')
		f1.write('g = game.Game(config=\'' + g.game.fen() + '\')\n')
		f1.write('e = eval.ChessAI(g, params=' + str(mutParams) + ')\n')
		f1.write('moves = 0\n')
		f1.write('while moves < 10 and not g.over() and not g.isDraw():\n')
		f1.write('\t moves += 1\n')
		f1.write('\tscore, move = e.nextMove()\n')
		f1.write('\tg.move(move)\n')
		f1.write('print e.eval()')
		f2 = open('mutant' + str(i) + 'a.sh', 'w')
		f2.write('#!/bin/bash\n')
		f2.write('#SBATCH -t 15\n')
		f2.write('#SBATCH -p serial_requeue\n')
		f2.write('#SBATCH -N 1\n')
		f2.write('#SBATCH -c 4\n')
		f2.write('#SBATCH --mem=16000\n')
		f2.write('#SBATCH -o mutant' + str(i) + 'a.out\n')
		f2.write('#SBATCH -e mutant' + str(i) + 'a.err\n')
		f2.write('#SBATCH --mail-type=END\n')
		f2.write('#SBATCH --mail-user=benjaminzheng@college.harvard.edu\n')
		f2.write('python mutant' + str(i) + 'a.py')

		f1.close()
		f2.close()

		call(["sbatch", "mutant" + str(i) + "a.sh"])

	best = -99999999999.0
	for i in range(5):
		done = False
		while not done:
			if os.path.exists('mutant' + str(i) + 'a.out') and os.path.getsize('mutant' + str(i) + 'a.out') > 0:
				done = True
		f3 = open('mutant' + str(i) + 'a.out', 'r')
		# Parse and find best score
		result = float(f3.readlines()[-1])
		f3.close()
		if result >best:
			best = result
			curParams = allMuts[i]

	standard = eval.ChessAI(g, params=curParams)
	score, move = standard.nextMove()
	g.move(move)
	print("Move #" + str(moves) + ":")
	print("Move: " + str(move))
	print("Score: " + str(score))
	print("Params: " + str(curParams))