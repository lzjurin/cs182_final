import chess, game
import os, sys
from collections import deque

class ChessAI:
    def __init__(self, gamestate, params=[0.025,0.025,0.0125,0.0125,0.0067,0.033,0.005,0.02,1]):
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

    # Returns the difference in the amount of material on each side of the board, with a positive return value showing a white advantage
    def material(self,side=-1):
        whiteScore = len(self.gamestate.pieces(True,1)) + 3 * (len(self.gamestate.pieces(True,2)) + len(self.gamestate.pieces(True,3))) + 5 * len(self.gamestate.pieces(True,4)) + 9 * len(self.gamestate.pieces(True,5))
        blackScore = len(self.gamestate.pieces(False,1)) + 3 * (len(self.gamestate.pieces(False,2)) + len(self.gamestate.pieces(False,3))) + 5 * len(self.gamestate.pieces(False,4)) + 9 * len(self.gamestate.pieces(False,5))
        if side == -1:
            return  whiteScore - blackScore
        if side == 0:
            return blackScore
        if side == 1:
            return whiteScore

    # Returns a yuge bonus for find a checkmate move
    def checkmate(self):
        if self.gamestate.game.is_checkmate():
            if self.gamestate.turn() == "White":
                return -5000
            elif self.gamestate.turn() == "Black":
                return 5000
        return 0

    # Returns the difference in the amount of available squares on each side of the board, with a white advantage being positive
    def space(self):
        if self.gamestate.turn == "White":
            return len(self.gamestate.available()[0]) - len(self.gamestate.available()[1])
        else:
            return len(self.gamestate.available()[1]) - len(self.gamestate.available()[0])

    # Returns a value reflecting the defensive and offensive state of each team
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
                # Awards points for defending pieces
                for friendlyPiece in self.gamestate.threatened()[0][y][x]:
                    if friendlyPiece[1] in self.gamestate.BLesserValue[n]:
                        wSum += .25
                    pieceThreat -= 1
                # Determines if piece is in danger of being taken
                if pieceThreat > 0 and smallerThreat:
                    wSum -= self.gamestate.values[n]
                # Assesses penalty for all pins
                if self.gamestate.pinned(y*8 + x):
                    if n == 6:
                        wSum -= 9
                    else:
                        wSum-= self.gamestate.values[n]
                # Assesses penalty for all forks
                if self.gamestate.forked(y*8 + x):
                    if n == 6:
                        wSum -= 9
                    else:
                        wSum -= self.gamestate.values[n]
            # Repeats process for black pieces
            for y,x in bPieces:
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
    # Returns difference in mobility between white and black
    def mobility(self):
        return len(self.gamestate.legalMoves(color=True)) - len(self.gamestate.legalMoves(color=False))

    # Returns a tuple of the best next move and the value associated with it, in the form (val,move)
    def nextMove(self, depth=1):
        if not depth:
            return (self.eval(), None)
        func = min if (depth & 1) ^ int(self.gamestate.turn_bool()) else max
        vals = []
        turn = self.gamestate.turn_bool()
        for move in self.gamestate.legalMoves():
            print(chr(27) + "[2J")
            print self.gamestate
            movestack = deque(map(lambda move: chess.Move.from_uci(move.uci()), list(self.gamestate.game.move_stack)))
            fen = self.gamestate.game.board_fen()
            self.gamestate.move(move)
            self.gamestate.game.turn = turn
            vals.append(self.nextMove(depth - 1)[0])
            self.gamestate.game.set_board_fen(fen)
            self.gamestate.game.move_stack = movestack
        val = func(vals)
        return (val, self.gamestate.legalMoves()[vals.index(val)])

    # Calls all subevaluation functions, returns result of adding them together and weighting with parameters
    def eval(self):
        return sum(map(lambda (x, y): float(x) * y, zip(self.params, [self.threat(), self.material(), self.space(),self.pieceSpecific(),self.pieceValues(),self.pawnStructure(), self.kingSafety(), self.mobility(),self.checkmate()])))

    # Returns the best move
    def moveEval(self):
        moves = []
        for move in self.gamestate.legalMoves():
            c = ChessAI(self.gamestate.move(move))
            moves.append(c.eval(),move)
        return max(moves)[1]

    # Returns bonus or penalty for each piece depending on where it is on the board, index tables taken from https://chessprogramming.wikispaces.com/Simplified+evaluation+function
    def pieceValues(self):
        def helper(isWhite):
            total = 0
            # Iterates over all possible classes of pieces
            for n in range (1,7):
                # Iterates over all pieces for the given color
                pieces = self.gamestate.pieces(isWhite,n)
                for (y,x) in pieces:
                    if isWhite:
                        # Allows for differentiation of end game king versus early and mid game king positioning needs
                        if n == 6 and self.material(int(not isWhite)) < 13:
                            total += self.index[n+1][x][y]
                        else:
                            total += self.index[n][x][y]
                    else:
                        if n == 6 and self.material(int(not isWhite)) < 13:
                            total += self.index[n+1][x][7-y]
                        else:
                            total += self.index[n][x][7-y]
            return total
        return helper(True) - helper(False)

    # Returns bonuses for certain positions, including pawn outposts and rooks being on open files
    def pieceSpecific(self):
        def helper(isWhite):
            # Initializes positions
            total = 0
            pawns = self.gamestate.pieces(isWhite,1)
            knights = self.gamestate.pieces(isWhite,2)
            bishops = self.gamestate.pieces(isWhite,3)
            rooks = self.gamestate.pieces(isWhite,4)
            queen = self.gamestate.pieces(isWhite,5)
            # Gives bonus for pawns storming a castled king
            for (y,x) in pawns:
                # Enemy king Y, Enemy king X
                eKY,eKX = self.gamestate.pieces(not isWhite,6)[0]
                if abs(eKX - x) <= 1:
                    total += 1.0/max(abs(eKY - y),1)
            if isWhite:
                # Gives bonus for knight being on a pawn outpost
                for (y,x) in knights:
                    if chess.Piece.from_symbol('P') in self.gamestate.threatened()[int(not isWhite)][y][x] and not [(py,px) for (py,px) in self.gamestate.pieces(isWhite,1) if abs(px-x) <= 1 and px != x and py > y]:
                        total += 5
                # Gives bonus for bishop being on a pawn outpost
                for (y,x) in bishops:
                    if chess.Piece.from_symbol('P') in self.gamestate.threatened()[int(not isWhite)][y][x] and not [(py,px) for (py,px) in self.gamestate.pieces(isWhite,1) if abs(px-x) <= 1 and px != x and py > y]:
                        total += 3
                # Gives bonus for being on open file and for threatening enemy rows of pawns
                for (y,x) in rooks:
                    enemyPawns = self.gamestate.pieces(not isWhite,1)
                    pawnsInRow = filter(lambda (py,px): y == py, enemyPawns)
                    if pawnsInRow > 1:
                        total += 4
                    pawnsInFile = filter(lambda (py,px): x == px, enemyPawns + pawns)
                    if pawnsInFile == 0:
                        total += 2
            # Does the same for the other color
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

    # Gives bonuses for having supporting and passed pawns, gives penalties for having backwards, isolated, or stacked pawns
    def pawnStructure(self):
        def helper(isWhite):
            total = 0
            # Gets pawn positions
            pawns = self.gamestate.pieces(isWhite,1)
            differentXValues=[]
            for y,x in pawns:
                if isWhite:
                    # Awards bonus for supporting pawns
                    for piece in self.gamestate.threatened()[0][y][x]:
                        if piece == chess.Piece.from_symbol('P'):
                            total += 1
                else:
                    # Awards bonus for supporting pawns to black team
                    for piece in self.gamestate.threatened()[1][y][x]:
                        if piece == chess.Piece.from_symbol('p'):
                            total += 1
                # Awards bonus for passed pawns
                if not filter(lambda (a,b): b==x or b==x-1 or b==x+1, self.gamestate.pieces(not isWhite,1)):
                    total += 3
                # Assesses penalties for isolated pawns
                if not filter(lambda (a,b): b==x-1 or b==x+1, self.gamestate.pieces(isWhite,1)):
                    total -= 2
                if x not in differentXValues:
                    differentXValues.append(x)
            # Assesses penalties for stacked pawns
            total -= (len(pawns) - len(differentXValues))
            if isWhite:
                # Assesses penalty for backwards pawns
                if len([(y,x) for (y,x) in pawns if y == min(pawns)[0]]) == 1 and chess.Piece.from_symbol('p') in self.gamestate.threatened()[1][y+1][x]:
                    total -= 3
            else:
                # Assesses penalty for backwards pawns for black
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
            # Awards bonus for castling
            if self.gamestate.hasCastled(color=isWhite):
                total += 100
                pawns = self.gamestate.pieces(isWhite,1)
                if isWhite:
                    # Awards bonus for protecting king with pawns in whichever direction the king castled
                    for p in pawns:
                        if p == (y+1,x) or p == (y+1,x+1) or p == (y+1,x-1):
                            total += 10
                else:
                    # Does the same for black
                    for p in pawns:
                        if p == (y-1,x) or p == (y-1,x+1) or p == (y-1,x-1):
                            total += 10
            # Initializes king zone
            kingZone = self.gamestate.kingzone(isWhite)
            if self.material(int(not isWhite)) > 12:
                subtotal = 0
                totalAttackingPieces = 0
                attackingPieces = []
                # Counts number of attacking pieces and rank of attacking pieces, assesses penalty using formula given on website
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
            # Disables king zone for end game, since king needs to be more aggressive
            else:
                return total
        return helper(True) - helper(False)
