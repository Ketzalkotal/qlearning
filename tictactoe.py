import random

qdict = {}
xwins = False
owins = False
# swap shift and up and swap capslock and esc
# figure out how to initialize this qmatrix
# write a rough of the algorithm

def applyMove(r, c, piece, board):
	# deep copy
	board = [b[:] for b in board]
	board[r][c] = piece
	return board

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
	return moves

def getmax(moveslist):
	best = max(moveslist, key=lambda x: x[1])
	if best[1] == 0:
		best = random.choice(moveslist)
	return best


def episode():
	initial = [['', '', ''],['', '', ''],['', '', '']]
	board = initial
	xwins = False
	owins = False
	for i in range(5):
		try:
			board = getmax(nextMove(board, 'x'))[0]
		except:
			break
		print 'x:'
		printBoard(board)
		if xwins:
			xwins = False
			break
		try:
			board = getmax(nextMove(board, 'o'))[0]
		except:
			break
		print 'o:'
		printBoard(board)
		if owins:
			owins = False
			break
	print 'game:', board

# initial = [['', '', ''],['', '', ''],['', '', '']]
# board = initial
# for i in range(5):
# 	try:
# 		board = getmax(nextMove(board, 'x'))[0]
# 	except:
# 		break
# 	print 'x:'
# 	printBoard(board)
# 	if xwins:
# 		xwins = False
# 		break
# 	try:
# 		board = getmax(nextMove(board, 'o'))[0]
# 	except:
# 		break
# 	print 'o:'
# 	printBoard(board)
# 	if owins:
# 		owins = False
# 		break
# print 'game:', board






# win = [['', 'x', ''],['o', 'x', 'o'],['', '', '']]
# # print legalMoves(base)
# # print legalMoves(first)
# moves = nextMove(win, 'x')
# gamma = 0.8
# print moves
# print getmax(moves)
# episode
# generate a random state
