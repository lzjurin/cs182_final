from game.game import *
from optparse import OptionParser
import time
from sys import stdin
import os

parser = OptionParser()
parser.add_option("-d", "--debug", action="store_true", dest="debug", default="True", help="Show state of game as you play")
(options, args) = parser.parse_args()

game = Game()

while not game.over():
    if options.debug:
        _=os.system("clear")
        print game
        print "{0} to move: ".format(game.turn())
    move = stdin.readline().strip()
    try:
        game.move(move)
    except ValueError as e:
        pass
