from collections import namedtuple
import logging
import copy

logging.basicConfig(
    filename='v2.log', level=logging.INFO, format='%(asctime)s %(message)s')
Move = namedtuple('Move', ['r', 'c'])

# BoardBase = namedtuple('BoardBase', [0, 1, 2])

class Board(Object):

    def __init__(self):
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]

    def play(self, move, piece):
        if self.board[move.r][move.c] == '':
            self.board[move.r][move.c] = piece
            return True
        # illegal move
        return False

    def __hash__(self):
        nboard = copy.deepcopy(self.board)
        return tuple([tuple(x[:]) for x in nboard]).__hash__()

    def clone(self):
        newboard = Board()
        newboard.board = [x[:] for x in self.board]
        return newboard

    def getTup(self):
        return tuple([tuple(x[:]) for x in self.board])

    def setTup(self, tup):
        self.board = [x[:] for x in tup]

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not (self.__hash__() == other.__hash__())

    def __str__(self):
        return '\n'.join([str(row) for row in self.board])

class QDict(object):
    def __init__(self):
        self.qdict = {}

    def getBoard(self, board):
        return self.qdict.get(board, None)

    def getScore(self, board, move):
        return self.qdict[board][move]

    def setScore(self, board, move, score):
        if not (board in self.qdict):
            self.qdict[board] = {}
        if not (move in self.qdict[board]):
            self.qdict[board][move] = 0
        self.qdict[board][move] = score

qdicts = {'x': QDict(), 'o': QDict()}

board = Board()
move = Move(1,1)
print board
qdicts['x'].setScore(board, move, 50)
board.play(move, 'x')

print qdicts['x'].qdict
print qdicts['x'].getScore(Board(), Move(1,1))
# board = Board()
# board.play(Move(1, 1), 'x')
# a = {board: 10}
# b = {Move(1,2): 20}
# board2 = Board()
# board2.play(Move(1, 1), 'x')
# board.play(Move(0, 1), 'o')
# print board
# print board2
# print b[Move(1,2)]