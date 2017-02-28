import random
import traceback

random.seed(1000)

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
    aboard = boardT2L(board)
    newBoard = [b[:] for b in aboard]
    newBoard[r][c] = piece
    return boardL2T(newBoard)

def _printBoard(board):
    print board[0]
    print board[1]
    print board[2]

def possibleMoves(board):
    moves = []
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell is '':
                moves.append((r, c))
    if moves is []:
        print 'moves is empty'
        print traceback.format_exc()
    return moves

def qSet(piece, board, action, score):
    if not (board in qdict[piece]):
        qdict[piece] = {board: {action: score}}
    else:
        qdict[piece][board][action] = score

def qGet(piece, board, action):
    if not (board in qdict[piece]):
        qdict[piece][board] = {action: 0}
        return 0
    if not (action in qdict[piece][board]):
        qdict[piece][board][action] = 0
        return 0
    return qdict[piece][board][action]

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
def getMax(moveScores, piece):
    if len(moveScores) == 0:
        return None
    try:
        best = max(moveScores, key=lambda x: x[1])
    except:
        print 'ms:', moveScores
        print traceback.format_exc()
        return None
    if best[1] == 0:
        # if they're all 0 then randomly pick one
        best = random.choice(moveScores)
    return best

gamma = 0.8
GAMMA = gamma

def getMovesQScores(board, moves, piece):
    moveScores = []
    for move in moves:
        moveScores.append((move, qGet(piece, board, move)))
    return moveScores

def getMovesRScores(board, moves, piece):
    moveScores = []
    for move in moves:
        moveScores.append((move, R(board, move[0], move[1], piece)))
    return moveScores

def evaluate(nboard, piece):
    # what this should do is randomly place opposing piece everywhere
    # then evaluate next best move
    opponent = 'o' if piece is 'x' else 'x'
    print 'currentBoard', _printBoard(nboard), 'opponent', opponent
    opponentMoves = possibleMoves(nboard)
    print 'opponentMoves', opponentMoves
    boardPrimes = []
    for move in opponentMoves:
        r = move[0]
        c = move[1]
        oboard = applyMove(r, c, opponent, nboard)
        print 'oboard', oboard
        moveScores = getMovesQScores(oboard, possibleMoves(oboard), piece)
        print 'moveScores', moveScores
        moveScore = getMax(moveScores, piece)
    # is highest possible score
    print 'movescore:', moveScore
    if moveScore is None:
        return None
    return moveScore[1]

def makeMove(board, piece, printBool):
    moves = possibleMoves(board)
    moveScores = getMovesQScores(board, moves, piece)
    moveScore = getMax(moveScores, piece)
    # move is best move from current board
    move = moveScore[0]
    qscore = moveScore[1]
    # asdfasdf
    nboard = applyMove(move[0], move[1], piece, board)
    nqscore = evaluate(nboard, piece)
    # move is best move from current board
    score = R(board, move[0], move[1], piece) + (GAMMA * nqscore)
    if R(board, move[0], move[1], piece) == 100:
        if piece is 'x':
            xwins = True
        if piece is 'o':
            owins = True
    qSet(piece, board, move, score)
    # print for debug
    if printBool:
        print 'piece', piece
        _printBoard(nboard)
    return nboard

# an episode is a game
def episode(printBool):
    global xwins
    global owins
    board = (('', '', ''),('', '', ''),('', '', ''))
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

for i in range(5):
    episode(True)
