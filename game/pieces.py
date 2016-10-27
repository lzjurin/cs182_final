import sys

class InvalidPieceError(Exception):
    def __init__(self, piece, err):
        self.piece = piece
        self.err = err

    def __str__(self):
        return "{0} {1}".format(self.piece, self.err)

class AbstractPiece(object):
    def __init__(self, position=None, value=None, player=None):
        self.position = position
        self.value = value
        self.player = player

    def moves(self):
        raise NotImplementedError("Abstract class AbstractPiece has no moves")

    def __value__(self):
        raise NotImplementedError("Abstract class AbstractPiece has no value")

    def __position__(self):
        raise NotImplementedError("Abstract class AbstractPiece has no position")

    def __str__(self):
        return "AbstractPiece"

    def charRep(self):
        raise NotImplementedError("Abstract class AbstractPiece has no grid representation")

    def getPlayer(self):
        raise NotImplementedError("Abstract class AbstractPiece has no player")

    getVal = __value__
    getPos = __position__
    getStr = __str__
    __repr__ = __str__

class GenericPiece(AbstractPiece):
    def __init__(self, position=None, value=None, player=None):
        if type(position).__name__ == type(value).__name__ == 'int' and self.defaultvalue:
            super(GenericPiece, self).__init__((position, value), self.defaultvalue, player)
        else:
            super(GenericPiece, self).__init__(position, value if value else self.defaultvalue, player)
        self.validate()
        self.linear = True

    def validate(self):
        if not self.position:
            raise InvalidPieceError(self, "must be created with a position in format (i, j)")
        elif not (type(self.position).__name__ == 'tuple' and type(self.position[0]).__name__ == type(self.position[1]).__name__ == 'int'):
            raise InvalidPieceError(self, "has invalid position {0}".format(self.position))

        if not self.value:
            raise InvalidPieceError(self, "must be created with a value")
        elif type(self.value).__name__ != 'int':
            raise InvalidPieceError(self, "cannot be created with noninteger value {0}".format(self.value))
        elif self.value < 1:
            raise InvalidPieceError(self, "cannot be created with nonpositive value {0}".format(self.value))

    def moves(self):
        return []

    def __value__(self):
        return self.value

    def __position__(self):
        return self.position

    def __str__(self):
        return "Piece type {0} at position {1} with value {2}".format(self.__class__, self.position, self.value)

    def charRep(self, ini=None):
        ini = ini if ini else self.__class__.__name__[0]
        return ini if self.player == "White" else ini.lower()

    def getPlayer(self):
        if not self.player:
            raise InvalidPieceError(self, "Dobby has no master")
        return self.player

    def getClass(self):
        return self.__class__

    def getType(self):
        return self.getClass().__name__

    def setPosition(self, position):
        if position in self.moves():
            self.position = position
            return True
        return False


    getVal = __value__
    getPos = __position__
    getStr = __str__
    __repr__ = __str__

class Pawn(GenericPiece):
    def __init__(self, position=None, value=None, player="White"):
        self.defaultvalue = 1
        super(self.__class__, self).__init__(position, value, player)

    def moves(self):
        return [ (self.position[0] + y, self.position[1]) for y in (range(1, 3) if self.player == "Black" else range(-2, 0))]

    def promoteable(self):
        return not self.position[1] % 7

class Bishop(GenericPiece):
    def __init__(self, position=None, value=None, player="White"):
        self.defaultvalue = 3
        super(self.__class__, self).__init__(position, value, player)

    def moves(self):
        # Flatten the lists of moves across directions
        return reduce(lambda x, y: x + y,

            # Iterate over directions and go up to 7 moves in that direction
            map(lambda dir:
                map(lambda dist: (self.position[0] + dir[0] * dist, self.position[1] + dir[1] * dist), range(1, 8)),

                    # Directions of movement
                    [ (-1, -1), (-1, 1), (1, -1), (1, 1) ] ) )

class Rook(GenericPiece):
    def __init__(self, position=None, value=None, player="White"):
        self.defaultvalue = 5
        super(self.__class__, self).__init__(position, value, player)

    def moves(self):
        # Flatten the lists of moves across directions
        return reduce(lambda x, y: x + y,

            # Iterate over directions and go up to 7 moves in that direction
            map(lambda dir:
                map(lambda dist: (self.position[0] + dir[0] * dist, self.position[1] + dir[1] * dist), range(1, 8)),

                    # Directions of movement
                    [ (0, 1), (1, 0), (0, -1), (-1, 0) ] ) )

class Queen(GenericPiece):
    def __init__(self, position=None, value=None, player="White"):
        self.defaultvalue = 9
        super(self.__class__, self).__init__(position, value, player)

    def moves(self):
        # Flatten the lists of moves across directions
        return reduce(lambda x, y: x + y,

            # Iterate over directions and go up to 7 moves in that direction
            map(lambda dir:
                map(lambda dist: (self.position[0] + dir[0] * dist, self.position[1] + dir[1] * dist), range(1, 8)),

                    # Directions of movement
                    [ (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) ] ) )

class King(GenericPiece):
    def __init__(self, position=None, value=None, player="White"):
        self.defaultvalue = sys.maxint
        super(self.__class__, self).__init__(position, value, player)

    def moves(self):
        # Map directions across the position
        return map(lambda dir: (self.position[0] + dir[0], self.position[1] + dir[1]),
            [ (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) ] )

class Knight(GenericPiece):
    def __init__(self, position=None, value=None, player="White"):
        self.defaultvalue = 3
        super(self.__class__, self).__init__(position, value, player)
        self.linear = False

    def moves(self):
        # Map directions across the position
        return map(lambda dir: (self.position[0] + dir[0], self.position[1] + dir[1]),
            [ (-2, -1), (-1, -2), (-1, 2), (2, -1), (2, 1), (1, 2), (1, -2), (-2, 1) ] )

    def charRep(self, ini='N'):
        return super(self.__class__, self).charRep(ini=ini)
