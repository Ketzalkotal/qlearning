import unittest
from collections import namedtuple
import logging
import copy

logging.basicConfig(
    filename='v2.log', level=logging.INFO, format='%(asctime)s %(message)s')
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
    score = 0
    clone = board.clone()
    r = move.r
    c = move.c
    # set reward for win states
    # horizontal
    if clone.board[r][(c - 1) % 3] == piece and clone.board[r][(c + 1) % 3] == piece:
        score = 100
    # vertical
    if clone.board[(r - 1) % 3][c] == piece and clone.board[(r + 1) % 3][c] == piece:
        score = 100
    # diagonal to left
    if r == c and clone.board[(r - 1) % 3][(c - 1) % 3] == piece and clone.board[(r + 1) % 3][(c + 1) % 3] == piece:
        score = 100
    # diagonal to right
    if (r + 2) % 2 == (c - 2) % 2 and clone.board[(r - 1) % 3][(c + 1) % 3] == piece and clone.board[(r + 1) % 3][(c - 1) % 3] == piece:
        score = 100
    return score

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
        board.play(Move(0,0), 'x')
        board.play(Move(1,1), 'x')
        self.assertTrue(R(board, Move(2,2), 'x') == 100)

    def test_win_forward_diagonal(self):
        board = Board()
        board.play(Move(0,2), 'x')
        board.play(Move(1,1), 'x')
        self.assertTrue(R(board, Move(2,0), 'x') == 100)

    def test_win_horizontal(self):
        board = Board()
        board.play(Move(0,0), 'x')
        board.play(Move(0,1), 'x')
        self.assertTrue(R(board, Move(0,2), 'x') == 100)

    def test_no_win_horizontal(self):
        board = Board()
        board.play(Move(1,0), 'x')
        board.play(Move(0,1), 'x')
        self.assertTrue(R(board, Move(0,2), 'x') == 0)

if __name__ == '__main__':
    qdicts = {'x': QDict(), 'o': QDict()}

    board = Board()
    move = Move(1, 1)

    qdicts['x'].setScore(board, move, 50)
    board.play(move, 'x')

    logging.info(qdicts['x'].qdict)
    logging.info(qdicts['x'].getScore(Board(), Move(1, 1)))
