from collections import namedtuple
import random

random.seed(1000)

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

    def _getTup(self):
        return tuple([tuple(x[:]) for x in self.board])

    def _setTup(self, tup):
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

    def bellman(self, qdict, move, piece):
        Qexpected = [0]
        opponent = 'o' if piece == 'x' else 'x'
        board = self.clone()
        boardA = self.clone()
        # currentScore = qdict.getScore(boardA, move)

        if boardA.play(move, piece):
            for opponentMove in boardA.possibleMoves():
                boardB = boardA.clone()
                boardB.play(opponentMove, opponent)
                for movePrime in boardB.possibleMoves():
                    Qexpected.append(qdict.getScore(boardB, movePrime))

            score = R(board, move, piece, opponent) + (qdict.gamma * (max(Qexpected)))
            qdict.setScore(board, move, score)
            return True
        return False

    def qlearn(self, qdict, piece):
        if self.isFull():
            return None
        opponent = 'x' if piece == 'o' else 'o'
        possibleMoves = self.possibleMoves()
        if len(possibleMoves) == 1:
            self.play(possibleMoves[0], piece)
            return True
            # no moves left
        if len(possibleMoves) == 0:
            # no moves left
            return False
        # eventually this must take a gamma to
        # control the randomness to minimize the randomness over time
        move = random.choice(possibleMoves)
        self.bellman(qdict, move, piece)
        self.play(move, piece)

    def qplay(self, qdict, piece):
        if self.isFull():
            return None
        opponent = 'x' if piece == 'o' else 'o'
        possibleMoves = self.possibleMoves()
        if len(possibleMoves) == 1:
            self.play(possibleMoves[0], piece)
            return True
            # no moves left
        if len(possibleMoves) == 0:
            # no moves left
            return False
        candidates = []
        ms = (random.choice(possibleMoves),0)
        for move in possibleMoves:
            score = qdict.getScore(self, move)
            if score > ms[1]:
                ms = (move, score)
        print ms[1]
        self.play(ms[0], piece)

    def __eq__(self, other):
        return self._getTup() == other

    def __ne__(self, other):
        return not (self._getTup() == other)

    def __str__(self):
        return '\n'.join([str(row) for row in self.board])


class QDict(object):

    def __init__(self, gamma=0.8):
        self.qdict = {}
        self.gamma = gamma

    def getBoard(self, board):
        return self.qdict.get(board._getTup(), 0)

    def getScore(self, board, move):
        result = 0
        if board._getTup() in self.qdict:
            result = self.qdict[board._getTup()].get(move, 0)
        return result

    def setScore(self, board, move, score):
        if not (board in self.qdict):
            self.qdict[board._getTup()] = {}
        if not (move in self.qdict[board]):
            self.qdict[board._getTup()][move] = 0
        self.qdict[board._getTup()][move] = score

def R(board, move, piece, opponent):
    clone = board.clone()
    clone.play(move, piece)
    # set reward for win states
    for oMove in clone.possibleMoves():
        opponentClone = clone.clone()
        opponentClone.play(oMove, opponent)
        if opponentClone.winTrue(opponent):
            return -100
    if clone.winTrue(piece):
        return 100
    return 0

qdicts = {'x': QDict(), 'o': QDict()}
def episode():
    board = Board()
    while not (board.winTrue('x') or board.winTrue('o') or board.isFull()):
        board.qlearn(qdicts['x'], 'x')
        if board.winTrue('x'):
            break
        board.qlearn(qdicts['o'], 'o')

def game():
    board = Board()
    while not (board.winTrue('x') or board.winTrue('o') or board.isFull()):
        board.qplay(qdicts['x'], 'x')
        print 'x\n', board
        if board.winTrue('x'):
            break
        board.qplay(qdicts['o'], 'o')
        print 'o\n', board
        print ''

if __name__ == '__main__':

    for i in range(10000):
        episode()

    print qdicts['x'].qdict.items()[:10]

    for i in range(3):
        game()
        print 'endgame'
