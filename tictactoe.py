import random

qdict = {'x': {}, 'o': {}}
#qdict = {'x': [[ ]], 'o': {}}
#qdict['x'][0][0][(board)]
#qdict[piece][board][row][column]
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
					print xwins, owins
				moves.append((applyMove(r, c, piece, board), score))
	print moves
	return moves

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
		nextBoardScore = getmax(nextMove(board, 'x'))
		nextBoard, nextScore = nextBoardScore
		qdict[piece][board] = score + (gamma * (nextScore - score))
		# print for debug
		if printBool:
			print piece
			printBoard(nextBoard)
		return nextBoardScore

def episode(printBool):
	xboardScore = ((('', '', ''),('', '', ''),('', '', '')), 0)
	oboardScore = ((('', '', ''),('', '', ''),('', '', '')), 0)
	xwins = False
	owins = False
	# update matrix values
	while not xwins and not owins:
		xboardScore = getNextBoardScore(xboardScore, 'x', printBool)
		if xwins:
			xwins = False
			break
		oboardScore = getNextBoardScore(oboardScore, 'o', printBool)
		if owins:
			owins = False
			break
	if printBool:
		print 'game:', board

# for i in range(1000):
# 	episode(False)

for i in range(5):
	episode(True)
