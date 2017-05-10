import unittest
from tictactoe import *

import logging
import logging.handlers

# logging.basicConfig(filename='v2.log', level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger('BasicLogger')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler('v2.log', maxBytes=2*1024*1024, backupCount=2)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(handler)

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
        self.assertTrue(R(board, Move(2, 2), 'x', 'o') == 100)

    def test_win_forward_diagonal(self):
        board = Board()
        board.play(Move(0, 2), 'x')
        board.play(Move(1, 1), 'x')
        self.assertTrue(R(board, Move(2, 0), 'x', 'o') == 100)

    def test_win_horizontal(self):
        board = Board()
        board.play(Move(0, 0), 'x')
        board.play(Move(0, 1), 'x')
        self.assertTrue(R(board, Move(0, 2), 'x', 'o') == 100)

    def test_no_win_horizontal(self):
        board = Board()
        board.play(Move(1, 0), 'x')
        board.play(Move(0, 1), 'x')
        self.assertTrue(R(board, Move(0, 2), 'x', 'o') == 0)

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
        logger.info(board.possibleMoves())
        self.assertFalse(True)
