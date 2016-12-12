import chess, game
import os, sys

class ChessAI:
    def __init__(self, gamestate, params=[1,1,1,1,1,1,1,1]):
        self.gamestate = gamestate
        self.params = params
        self.materialWeight = 1
        self.threatWeight = 1
        self.kingSafetyTotalAttackers={0:0,1:0,2:50,3:75,4:88,5:94,6:97,7:99,8:99,9:99,10:99}
        self.bKingSafetyThreats={chess.Piece.from_symbol('P'):1,chess.Piece.from_symbol('B'): 20,chess.Piece.from_symbol('N'): 20,chess.Piece.from_symbol('R'): 40, chess.Piece.from_symbol('Q'): 80}
        self.wKingSafetyThreats={chess.Piece.from_symbol('p'):1,chess.Piece.from_symbol('b'): 20,chess.Piece.from_symbol('n'): 20,chess.Piece.from_symbol('r'): 40, chess.Piece.from_symbol('q'): 80}
        self.pawnPositionBonus =  [[0, 0, 0, 0, 0, 0, 0, 0], [50, 50, 50, 50, 50, 50, 50, 50], [10, 10, 20, 30, 30, 20, 10, 10], [5, 5, 10, 25, 25, 10, 5, 5], [0, 0, 0, 20, 20, 0, 0, 0], [5, -5, -10, 0, 0, -10, -5, 5], [5, 10, 10, -20, -20, 10, 10, 5], [0, 0, 0, 0, 0, 0, 0, 0]]
        self.knightPositionBonus = [[-50, -40, -30, -30, -30, -30, -40, -50], [-40, -20, 0, 0, 0, 0, -20, -40], [-30, 0, 10, 15, 15, 10, 0, -30], [-30, 5, 15, 20, 20, 15, 5, -30], [-30, 0, 15, 20, 20, 15, 0, -30], [-30, 5, 10, 15, 15, 10, 5, -30], [-40, -20, 0, 5, 5, 0, -20, -40], [-50, -40, -30, -30, -30, -30, -40, -50]]
        self.bishopPositionBonus = [[-20, -10, -10, -10, -10, -10, -10, -20], [-10, 0, 0, 0, 0, 0, 0, -10], [-10, 0, 5, 10, 10, 5, 0, -10], [-10, 5, 5, 10, 10, 5, 5, -10], [-10, 0, 10, 10, 10, 10, 0, -10], [-10, 10, 10, 10, 10, 10, 10, -10], [-10, 5, 0, 0, 0, 0, 5, -10], [-20, -10, -10, -10, -10, -10, -10, -20]]
        self.rookPositionBonus = [[0, 0, 0, 0, 0, 0, 0, 0], [5, 10, 10, 10, 10, 10, 10, 5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [0, 0, 0, 5, 5, 0, 0, 0]]
        self.queenPositionBonus = [[-20, -10, -10, -5, -5, -10, -10, -20], [-10, 0, 0, 0, 0, 0, 0, -10], [-10, 0, 5, 5, 5, 5, 0, -10], [-5, 0, 5, 5, 5, 5, 0, -5], [0, 0, 5, 5, 5, 5, 0, -5], [-10, 5, 5, 5, 5, 5, 0, -10], [-10, 0, 5, 0, 0, 0, 0, -10], [-20, -10, -10, -5, -5, -10, -10, -20]]
        self.kingEarlyPositionBonus = [[-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-20, -30, -30, -40, -40, -30, -30, -20], [-10, -20, -20, -20, -20, -20, -20, -10], [20, 20, 0, 0, 0, 0, 20, 20], [20, 30, 10, 0, 0, 10, 30, 20]]
        self.kingLatePositionBonus = [[-50, -40, -30, -20, -20, -30, -40, -50], [-30, -20, -10, 0, 0, -10, -20, -30], [-30, -10, 20, 30, 30, 20, -10, -30], [-30, -10, 30, 40, 40, 30, -10, -30], [-30, -10, 30, 40, 40, 30, -10, -30], [-30, -10, 20, 30, 30, 20, -10, -30], [-30, -30, 0, 0, 0, 0, -30, -30], [-50, -30, -30, -30, -30, -30, -30, -50]]
        self.index = {1: self.pawnPositionBonus, 2: self.knightPositionBonus, 3: self.bishopPositionBonus, 4: self.rookPositionBonus, 5: self.queenPositionBonus, 6: self.kingEarlyPositionBonus, 7: self.kingEarlyPositionBonus}

    def material(self,side=-1):
        whiteScore = len(self.gamestate.pieces(True,1)) + 3 * (len(self.gamestate.pieces(True,2)) + len(self.gamestate.pieces(True,3))) + 5 * len(self.gamestate.pieces(True,4)) + 9 * len(self.gamestate.pieces(True,5))
        blackScore = len(self.gamestate.pieces(False,1)) + 3 * (len(self.gamestate.pieces(False,2)) + len(self.gamestate.pieces(False,3))) + 5 * len(self.gamestate.pieces(False,4)) + 9 * len(self.gamestate.pieces(False,5))
        if side == -1:
            return  whiteScore - blackScore
        if side == 0:
            return blackScore
        if side == 1:
            return whiteScore

    # def advance(self):
    #     wSum = 0
    #     bSum = 0
    #     for n in range(1,6):
    #         for piece in self.gamestate.pieces(True,n):
    #             wSum += min(1,piece[0]/float(4))
    #         for piece in self.gamestate.Bpieces:
    #             bSum += int(piece[-1])
    #     # for k in self.gamestate.Wknights:
    #     #     if '1' in k or '8' in k or 'a' in k or 'h' in k:
    #     #         wSum -= 1
    #     # for k in self.gamestate.Bknights:
    #     #     if '1' in k or '8' in k or 'a' in k or 'h' in k:
    #     #         bSum -= 1
    #     # for b in self.gamestate.Wbishops:
    #     #     if b == 'a1' or b == 'a8' or b=='h1' or b=='h8':
    #     #         wSum -= 1
    #     # for b in self.gamestate.Bknights:
    #     #     if b == 'a1' or b == 'a8' or b=='h1' or b=='h8':
    #     #         bSum -= 1
    #     return wSum - bSum
    # def pawns(self):
    def space(self):
        if self.gamestate.turn == "White":
            return len(self.gamestate.available()[0]) - len(self.gamestate.available()[1])
        else:
            return len(self.gamestate.available()[1]) - len(self.gamestate.available()[0])
        # wTotal = 0
        # bTotal = 0
        # for k in self.gamestate.available().keys():
        #     if k[0]<4:
        #         wTotal += 1
        #     else:
        #         bTotal += 1
        # return wTotal - bTotal
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
                if self.gamestate.pinned(y*8 + x):
                    if n == 6:
                        wSum -= 9
                    else:
                        wSum-= self.gamestate.values[n]
                if self.gamestate.forked(y*8 + x):
                    if n == 6:
                        wSum -= 9
                    else:
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
                if self.gamestate.pinned(y*8+x):
                    if n == 6:
                        bSum -= 9
                    else:
                        bSum-= self.gamestate.values[n]
                if self.gamestate.forked(y*8+x):
                    if n == 6:
                        bSum -= 9
                    else:
                        bSum -= self.gamestate.values[n]
        return wSum - bSum
    def mobility(self):
        return len(self.gamestate.legalMoves(color=True)) - len(self.gamestate.legalMoves(color=False))

    def nextMove(self, depth=1):
        if not depth:
            return (self.eval(), None)
        func = min if (depth & 1) ^ int(self.gamestate.turn_bool()) else max
        vals = []
        for move in self.gamestate.legalMoves():
            self.gamestate.move(move)
            vals.append(self.nextMove(depth - 1)[0])
            self.gamestate.undo()
        val = func(vals)
        return (val, self.gamestate.legalMoves()[vals.index(val)])

    def eval(self):
        return sum(map(lambda (x, y): float(x) * y, zip(self.params, [self.threat(), self.material(), self.space(),self.pieceSpecific(),self.pieceValues(),self.pawnStructure(), self.kingSafety(), self.mobility()])))

    def moveEval(self):
        moves = []
        for move in self.gamestate.available():
            c = ChessAI(self.gamestate.move(move))
            moves.append(c.eval(),move)
        return max(moves)[1]
    def pieceValues(self):
        def helper(isWhite):
            total = 0
            for n in range (1,7):
                pieces = self.gamestate.pieces(isWhite,n)
                for (y,x) in pieces:
                    if isWhite:
                        if n == 6 and self.material(int(not isWhite)) < 13:
                            total += self.index[n+1][x][7]
                        else:
                            total += self.index[n][x][y]
                    else:
                        if n == 6 and self.material(int(not isWhite)) < 13:
                            total += list(reversed(self.index[n+1]))[x][7]
                        else:
                            total += list(reversed(self.index[n]))[x][y]
            return total
        return helper(True) - helper(False)
    def pieceSpecific(self):
        def helper(isWhite):
            total = 0
            pawns = self.gamestate.pieces(isWhite,1)
            knights = self.gamestate.pieces(isWhite,2)
            bishops = self.gamestate.pieces(isWhite,3)
            rooks = self.gamestate.pieces(isWhite,4)
            queen = self.gamestate.pieces(isWhite,5)
            for (y,x) in pawns:
                # Enemy king Y, Enemy king X
                eKY,eKX = self.gamestate.pieces(not isWhite,6)[0]
                if abs(eKX - x) <= 1:
                    total += 1.0/abs(eKY - y)
            if isWhite:
                for (y,x) in knights:
                    if chess.Piece.from_symbol('P') in self.gamestate.threatened()[int(not isWhite)][y][x] and not [(py,px) for (py,px) in self.gamestate.pieces(isWhite,1) if abs(px-x) <= 1 and px != x and py > y]:
                        total += 5
                for (y,x) in bishops:
                    if chess.Piece.from_symbol('P') in self.gamestate.threatened()[int(not isWhite)][y][x] and not [(py,px) for (py,px) in self.gamestate.pieces(isWhite,1) if abs(px-x) <= 1 and px != x and py > y]:
                        total += 3
                for (y,x) in rooks:
                    enemyPawns = self.gamestate.pieces(not isWhite,1)
                    pawnsInRow = filter(lambda (py,px): y == py, enemyPawns)
                    if pawnsInRow > 1:
                        total += 4
                    pawnsInFile = filter(lambda (py,px): x == px, enemyPawns + pawns)
                    if pawnsInFile == 0:
                        total += 2
            else:
                for (y,x) in knights:
                    if chess.Piece.from_symbol('p') in self.gamestate.threatened()[int(not isWhite)][y][x] and not [(py,px) for (py,px) in self.gamestate.pieces(isWhite,1) if abs(px-x) <= 1 and px != x and py < y]:
                        total += 5
                for (y,x) in bishops:
                    if chess.Piece.from_symbol('p') in self.gamestate.threatened()[int(not isWhite)][y][x] and not [(py,px) for (py,px) in self.gamestate.pieces(isWhite,1) if abs(px-x) <= 1 and px != x and py < y]:
                        total += 3
                for (y,x) in rooks:
                    enemyPawns = self.gamestate.pieces(not isWhite,1)
                    pawnsInRow = filter(lambda (py,px): y == py, enemyPawns)
                    if pawnsInRow > 1:
                        total += 4
                    pawnsInFile = filter(lambda (py,px): x == px, enemyPawns + pawns)
                    if pawnsInFile == 0:
                        total += 2
            return total
        return helper(True) - helper(False)
    def pawnStructure(self):
        def helper(isWhite):
            total = 0
            pawns = self.gamestate.pieces(isWhite,1)
            differentXValues=[]
            for y,x in pawns:
                # if not filter(lambda (a,b): b==x, self.gamestate.pieces(not isWhite,1)):
                #     total += 1
                if isWhite:
                    for piece in self.gamestate.threatened()[0][y][x]:
                        if piece == chess.Piece.from_symbol('P'):
                            total += 1
                else:
                    for piece in self.gamestate.threatened()[1][y][x]:
                        if piece == chess.Piece.from_symbol('p'):
                            total += 1
                if not filter(lambda (a,b): b==x or b==x-1 or b==x+1, self.gamestate.pieces(not isWhite,1)):
                    total += 3
                if not filter(lambda (a,b): b==x-1 or b==x+1, self.gamestate.pieces(isWhite,1)):
                    total -= 2
                if x not in differentXValues:
                    differentXValues.append(x)
            total -= (len(pawns) - len(differentXValues))
            if isWhite:
                if len([(y,x) for (y,x) in pawns if y == min(pawns)[0]]) == 1 and chess.Piece.from_symbol('p') in self.gamestate.threatened()[1][y+1][x]:
                    total -= 3
            else:
                if len([(y,x) for (y,x) in pawns if y == min(pawns)[0]]) == 1 and chess.Piece.from_symbol('P') in self.gamestate.threatened()[1][y-1][x]:
                    total -= 3
            return total
        return helper(True) - helper(False)

    def kingSafety(self):
        whiteKingPos = self.gamestate.pieces(True,6)[0]
        blackKingPos = self.gamestate.pieces(False,6)[0]
        def helper(isWhite):
            (y,x) = self.gamestate.pieces(isWhite,6)[0]
            total = 0
            # CHANGE TO CHECK FOR IF CASTLED INSTEAD
            if True:
                total += 100
                pawns = self.gamestate.pieces(isWhite,1)
                if isWhite:
                    for p in pawns:
                        if p == (y+1,x) or p == (y+1,x+1) or p == (y+1,x-1):
                            total += 10
                else:
                    for p in pawns:
                        if p == (y-1,x) or p == (y-1,x+1) or p == (y-1,x-1):
                            total += 10
            # CHANGE TO REPRESENT ACTUAL KINGZONE
            kingZone = self.gamestate.kingzone(isWhite)
            if self.material(int(not isWhite)) > 12:
                subtotal = 0
                totalAttackingPieces = 0
                attackingPieces = []
                for y,x in kingZone:
                    for threat in self.gamestate.threatened()[int(isWhite)][y][x]:
                        if isWhite:
                            subtotal += self.wkingSafetyThreats[threat[1]]
                            if threat[0] in attackingPieces:
                                continue
                            else:
                                attackingPieces.append(threat[0])
                        else:
                            subtotal += self.bkingSafetyThreats[threat[1]]
                            if threat[0] in attackingPieces:
                                continue
                            else:
                                attackingPieces.append(threat[0])
                return total - (self.kingSafetyTotalAttackers[totalAttackingPieces] * subtotal)/100.0
            else:
                return total
        return helper(True) - helper(False)
