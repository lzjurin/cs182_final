import chess, game
import os, sys
class ChessAI:
    def __init__(self, gamestate, params=[1, 1]):
        self.gamestate = gamestate
        self.params = params
        self.materialWeight = 1
        self.threatWeight = 1
    def material(self):
        whiteScore = len(self.gamestate.pieces(True,1)) + 3 * (len(self.gamestate.pieces(True,2)) + len(self.gamestate.pieces(True,3))) + 5 * len(self.gamestate.pieces(True,4)) + 9 * len(self.gamestate.pieces(True,5))
        blackScore = len(self.gamestate.pieces(False,1)) + 3 * (len(self.gamestate.pieces(False,2)) + len(self.gamestate.pieces(False,3))) + 5 * len(self.gamestate.pieces(False,4)) + 9 * len(self.gamestate.pieces(False,5))
        return  whiteScore - blackScore
    def advance(self):
        wSum = -self.gamestate.pieces(True,6)[0][0]
        bSum = 8 - self.gamestate.pieces(False,6)[0][0]
        for n in range(1,6):
            for piece in self.gamestate.pieces(True,n):
                wS += min(1,piece[0]/float(4)) if
            for piece in self.gamestate.Bpieces:
                bSum += int(piece[-1])
        for k in self.gamestate.Wknights:
            if '1' in k or '8' in k or 'a' in k or 'h' in k:
                wSum -= 1
        for k in self.gamestate.Bknights:
            if '1' in k or '8' in k or 'a' in k or 'h' in k:
                bSum -= 1
        for b in self.gamestate.Wbishops:
            if b == 'a1' or b == 'a8' or b=='h1' or b=='h8':
                wSum -= 1
        for b in self.gamestate.Bknights:
            if b == 'a1' or b == 'a8' or b=='h1' or b=='h8':
                bSum -= 1
        return wSum - bSum
    # def pawns(self):
    def space(self):
        wTotal = 0
        bTotal = 0
        for k in self.gamestate.available().keys():
            if k[0]<4:
                wTotal += 1
            else:
                bTotal += 1
        return wTotal - bTotal
    def threat(self):
        wSum = 0
        bSum = 0
        for n in range(1,7):
            # Get White and Black pieces
            wPieces = self.gamestate.pieces(True,n)
            bPieces = self.gamestate.pieces(False,n)
            # Get coordinates of white pieces
            for y,x in wPieces:
                # Get coordinates of attacking pieces
                pieceThreat = 0
                smallerThreat = False
                for enemyPiece in self.gamestate.threatened()[1][y][x]:
                    # Checks if enemy piece is worth less
                    if enemyPiece[1] in self.gamestate.WLesserValue[n]:
                        wSum -= 1
                        smallerThreat = True
                    pieceThreat += 1
                for friendlyPiece in self.gamestate.threatened()[0][y][x]:
                    if friendlyPiece[1] in self.gamestate.BLesserValue[n]:
                        wSum += .25
                    pieceThreat -= 1
                if pieceThreat > 0 and smallerThreat:
                    wSum -= self.gamestate.values[n]
            for y,x in bPieces:
                # Get coordinates of attacking pieces
                pieceThreat = 0
                smallerThreat = False
                for enemyPiece in self.gamestate.threatened()[0][y][x]:
                    if enemyPiece[1] in self.gamestate.BLesserValue[n]:
                        bSum -= 1
                        smallerThreat = True
                    pieceThreat += 1
                for friendlyPiece in self.gamestate.threatened()[1][y][x]:
                    if friendlyPiece[1] in self.gamestate.WLesserValue[n]:
                        bSum += .25
                        pieceThreat -= 1
                if pieceThreat > 0 and smallerThreat:
                    bSum -= self.gamestate.values[n]
        return wSum - bSum

    def nextMove(self, depth=1):
        if not depth:
            return (self.eval(), None)
        func = max if (depth & 1) == int(self.gamestate.turn_bool()) else min
        vals = []
        for move in self.gamestate.legalMoves():
            self.gamestate.move(move)
            vals.append(self.nextMove(depth - 1)[0])
            self.gamestate.undo()
        val = func(vals)
        return (val, self.gamestate.legalMoves()[vals.index(val)])


    def eval(self):
        return sum(map(lambda (x, y): float(x) * y, zip(self.params, [self.threat(), self.material()])))
    def moveEval(self):
        moves = []
        for move in self.legalMoves():
            c = ChessAI(self.gamestate.move(move))
            moves.append(c.eval(),move)
        return max(moves)[1]
    def kingSafety(self):
        whiteKingPos = self.gamestate.pieces(True,6)[0]
        blackKingPos = self.gamestate.pieces(False,6)[0]
        def helper(self, isWhite):
            y,x = self.gamestate.pieces(isWhite,6)[0]
            total = 0
            if castled:
                total += 5
                pawns = self.gamestate.pieces(isWhite,1)
                if isWhite:
                    for p in pawns:
                        if p == (y+1,x) or p == (y+1,x+1) or p == (y+1,x-1):
                            total += 1
                else:
                    for p in pawns:
                        if p == (y-1,x) or p == (y-1,x+1) or p == (y-1,x-1):
                            total += 1
            kingZone = self.gamestate.
