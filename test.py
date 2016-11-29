from game.game import *
from game.eval import *

newgame = Game()
ev = ChessAI(newgame)

print ev.eval()
newgame.move_san("Nc3")
newgame.move_san("Nc6")
newgame.move_san("d4")

print ev.eval()
