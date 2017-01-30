import random

#qdict[(board, piece)][(row,column)] = score
#qdict[piece][board][(row,column)] = score
#board = ((),(),())
qdict = {'x':{}, 'o':{}}

#qdict = {'x': [[ ]], 'o': {}}
#qdict['x'][0][0][(board)]
# the qdict represents a 4 dimensional coordinate which returns a score
# if that score doesn't exist the object is initialized
xwins = False
owins = False

def boardL2T(board):
    return tuple([tuple(b[:]) for b in board])

def boardT2L(board):
    return [list(b[:]) for b in board]

def applyMove(r, c, piece, board):
    # deep copy
    board = boardT2L(board)
    newBoard = [b[:] for b in board]
    newBoard[r][c] = piece
    return boardL2T(newBoard)

def printBoard(board):
    print board[0]
    print board[1]
    print board[2]

# R matrix
def nextMove(board, piece):
    moves = []
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            score = 0
            if cell is '':
                # set reward for win states
                # horizontal
                if board[r][(c - 1) % 3] == piece and board[r][(c + 1) % 3] == piece:
                    score = 100
                # vertical
                if board[(r - 1) % 3][c] == piece and board[(r + 1) % 3][c] == piece:
                    score = 100
                # diagonal to left
                if r == c and board[(r - 1) % 3][(c - 1) % 3] == piece and board[(r + 1) % 3][(c + 1) % 3] == piece:
                    score = 100
                # diagonal to right
                if (r + 2) % 2 == (c - 2) % 2 and board[(r - 1) % 3][(c + 1) % 3] == piece and board[(r + 1) % 3][(c - 1) % 3] == piece:
                    score = 100
                if score == 100:
                    xwins = piece == 'x'
                    owins = piece == 'o'
                moves.append((applyMove(r, c, piece, board), score))
    # each move is (board, score)
    return moves

def R(state, r, c, piece):
    board = applyMove(r, c, piece, state)
    score = 0
    # set reward for win states
    # horizontal
    if board[r][(c - 1) % 3] == piece and board[r][(c + 1) % 3] == piece:
        score = 100
    # vertical
    if board[(r - 1) % 3][c] == piece and board[(r + 1) % 3][c] == piece:
        score = 100
    # diagonal to left
    if r == c and board[(r - 1) % 3][(c - 1) % 3] == piece and board[(r + 1) % 3][(c + 1) % 3] == piece:
        score = 100
    # diagonal to right
    if (r + 2) % 2 == (c - 2) % 2 and board[(r - 1) % 3][(c + 1) % 3] == piece and board[(r + 1) % 3][(c - 1) % 3] == piece:
        score = 100
    return score

# you need next move q matrix

# Q(state, action) = R(state, action) + (gamma * max(all possible q scores from statePrime))
# statePrime is the state after action is applied
# all possible q scores is the list of all actions from statePrime

def getmax(moveslist):
    best = max(moveslist, key=lambda x: x[1])
    if best[1] == 0:
        # if they're all 0 then randomly pick one
        best = random.choice(moveslist)
    return best

gamma = 0.8
initial = ((('', '', ''),('', '', ''),('', '', '')), 0)
# an episode is a game
def getNextBoardScore(boardScore, piece, printBool):
        board, score = boardScore
        nextBoardScore = getmax(nextMove(board, piece))
        nextBoard, nextScore = nextBoardScore
        qdict[piece][board] = score + (gamma * (nextScore - score))
        # print for debug
        if printBool:
            print 'piece', piece
            printBoard(nextBoard)
        return nextBoardScore

def makeMove(board, piece, printBool):
        nextBoardScore = getmax(nextMove(board, piece))
        nextBoard, nextScore = nextBoardScore
        qdict[piece][board] = score + (gamma * (nextScore - score))
        # print for debug
        if printBool:
            print 'piece', piece
            printBoard(nextBoard)
        return nextBoardScore

def episode(printBool):
    xboardScore = ((('', '', ''),('', '', ''),('', '', '')), 0)
    oboardScore = ((('', '', ''),('', '', ''),('', '', '')), 0)
    xwins = False
    owins = False
    # update matrix values
    while not xwins and not owins:
        board = makeMove(board, 'x', printBool)
        # I want to pass the board between the two players
        if xwins:
            xwins = False
            break
        board = makeMove(board, 'o', printBool)
        if owins:
            owins = False
            break
    if printBool:
        print 'game:', board

# for i in range(1000):
#   episode(False)

for i in range(5):
    episode(True)
