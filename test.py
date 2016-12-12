from game.game import *
from game.eval import *

newgame = Game()
ev = ChessAI(newgame)

print ev.eval()
newgame.move_san("Nc3")
newgame.move_san("Nc6")
newgame.move_san("d4")

print ev.eval()
print ev.nextMove(1)

newgame = Game()
newgame.move(newgame.legalMoves()[-4])
newgame.move(newgame.legalMoves()[0])
newgame.move(newgame.legalMoves()[5])
print newgame

print newgame.pinned(53)
print newgame.forked(53)
