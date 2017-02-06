import unittest
from collections import namedtuple
import logging
import logging.handlers

# logging.basicConfig(filename='v2.log', level=logging.INFO, format='%(asctime)s %(message)s')
basic_logger = logging.getLogger('BasicLogger')
basic_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler('v2.log', maxBytes=20*1024*1024, backupCount=1)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
basic_logger.addHandler(handler)

Move = namedtuple('Move', ['r', 'c'])


class Board(object):

    def __init__(self):
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]

    def play(self, move, piece):
        if self.board[move.r][move.c] == '':
            self.board[move.r][move.c] = piece
            return True
        # illegal move
        return False

    def __hash__(self):
        b = self.clone()
        return tuple([tuple(x[:]) for x in b.board]).__hash__()

    def clone(self):
        newboard = Board()
        newboard.board = [x[:] for x in self.board]
        return newboard

    def getTup(self):
        return tuple([tuple(x[:]) for x in self.board])

    def setTup(self, tup):
        self.board = [x[:] for x in tup]

    def winTrue(self, piece):
        return ([piece, piece, piece] in
                [[self.board[0][0], self.board[1][0], self.board[2][0]],
                [self.board[0][1], self.board[1][1], self.board[2][1]],
                [self.board[0][2], self.board[1][2], self.board[2][2]],
                [self.board[0][0], self.board[1][1], self.board[2][2]],
                [self.board[0][2], self.board[1][1], self.board[2][0]]] or
                [piece, piece, piece] in self.board)

    def isFull(self):
        return not ('' in self.board[0] or
                    '' in self.board[1] or
                    '' in self.board[2])

    def possibleMoves(self):
        poss = []
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece == '':
                    poss.append(Move(r,c))
        return poss

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
        return self.qdict.get(board.__hash__(), None)

    def getScore(self, board, move):
        return self.qdict[board.__hash__()][move]

    def setScore(self, board, move, score):
        if not (board in self.qdict):
            self.qdict[board.__hash__()] = {}
        if not (move in self.qdict[board]):
            self.qdict[board.__hash__()][move] = 0
        self.qdict[board.__hash__()][move] = score

def R(board, move, piece):
    clone = board.clone()
    clone.play(move, piece)
    # set reward for win states
    if clone.winTrue(piece):
        return 100
    return 0

class BoardTest(unittest.TestCase):

    def test_equality(self):
        self.assertTrue(Board() == Board())

    def test_dict_equality(self):
        board1 = Board()
        board2 = Board()
        d = {board1: 10}
        self.assertTrue(d[board2] == 10)
        board1.play(Move(1, 1), 'x')
        board2.play(Move(1, 1), 'x')
        e = {board1: 20}
        self.assertTrue(e[board2] == 20)

    def test_qdict_equality_with_clone_play(self):
        move = Move(1, 1)
        board1 = Board()
        board2 = board1.clone()
        qdict = QDict()
        qdict.setScore(board1, move, 10)
        board3 = board1.clone()
        board3.play(move, 'x')
        self.assertTrue(qdict.getScore(Board(), move) == 10)

    def test_qdict_equality_with_del(self):
        move = Move(1, 1)
        board1 = Board()
        qdict = QDict()
        qdict.setScore(board1, move, 10)
        del(board1)
        self.assertTrue(qdict.getScore(Board(), move) == 10)

    def test_qdict_equality(self):
        move = Move(1, 1)
        board1 = Board()
        board2 = Board()
        qdict = QDict()
        qdict.setScore(board1, move, 10)
        board1.play(move, 'x')
        self.assertTrue(qdict.getScore(Board(), move) == 10)

    def test_win_diagonal(self):
        board = Board()
        board.play(Move(0, 0), 'x')
        board.play(Move(1, 1), 'x')
        self.assertTrue(R(board, Move(2, 2), 'x') == 100)

    def test_win_forward_diagonal(self):
        board = Board()
        board.play(Move(0, 2), 'x')
        board.play(Move(1, 1), 'x')
        self.assertTrue(R(board, Move(2, 0), 'x') == 100)

    def test_win_horizontal(self):
        board = Board()
        board.play(Move(0, 0), 'x')
        board.play(Move(0, 1), 'x')
        self.assertTrue(R(board, Move(0, 2), 'x') == 100)

    def test_no_win_horizontal(self):
        board = Board()
        board.play(Move(1, 0), 'x')
        board.play(Move(0, 1), 'x')
        self.assertTrue(R(board, Move(0, 2), 'x') == 0)

    def test_is_full(self):
        board = Board()
        board.board = [['x','x','x'],['x','x','x'],['x','x','x']]
        self.assertTrue(board.isFull())

    def test_is_not_full(self):
        board = Board()
        self.assertFalse(board.isFull())

    @unittest.skip('not finished yet')
    def test_poss_moves(self):
        board = Board()
        board.board = [['x','','x'],['x','x','x'],['x','x','x']]
        basic_logger.info(board.possibleMoves())
        self.assertFalse(True)

qdicts = {'x': QDict(), 'o': QDict()}
def episode():
    board = Board()
    while not (board.winTrue('x') or board.winTrue('o') or board.isFull()):
        board.qplay(qdicts['x'], 'x')
        board.qplay(qdicts['o'], 'o')

if __name__ == '__main__':

    board = Board()
    move = Move(1,1)
    qdicts['x'].setScore(board, move, 50)
    board.play(move, 'x')

    basic_logger.info(qdicts['x'].qdict)
    basic_logger.info(qdicts['x'].getScore(Board(), Move(1, 1)))
