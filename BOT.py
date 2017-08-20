import random
import time
import copy


class Player84:
	def __init__(self):
		self.INF = 10000000000
		self.bl_ut = [0,4,25,500,10000000000]
		self.bo_ut = [0,1,8,81,10000000]
		self.ccc = 0
		self.maxDepth = 0
		self.start_time = 0



	def find_empty_cells(self,board):
		
		validCells = []
		for i in range(16):
			for j in range(16):
				if board[i][j] == '-': validCells.append([i,j])
		return validCells


	def generate_random_cells(self,board):
		
		allowedMoves = []
		for i in range(16):
			for j in range(16):
				if board.board_status[i][j] == '-' and board.block_status[i/4][j/4] == '-':
					allowedMoves.append([i,j])
				
		return allowedMoves
        
	def find_valid_cells(self,board,old_move):
		
		x, y, emptyCells = (old_move[0]%4)*4, (old_move[1]%4)*4,[]
		if board.block_status[x/4][y/4] != '-': return []

		for i in range(4):
			for j in range(4):
				if board.board_status[x+i][y+j] == '-':emptyCells.append([x+i,y+j])
		return emptyCells

	def block_occupied(self,board,old_move,player):
		
		x, y, flag = (old_move[0]%4)*4, (old_move[1]%4)*4, 0
		
		if board.block_status[x/4][y/4] != '-': return 1
		
		return 0

	def calculate_utility_board(self,board,old_move,player,block,flag):
		# print "Y0"
		self.ccc += 1
		bo_ut=[]
		if player=='x': 
			bo_ut = self.bo_ut
		else: 
			for i in self.bo_ut: 
				bo_ut.append(-i)
		bo_sc = 0

		temp = [[] for i in range(4)]
		final = -10**12
		for i in range(4):
			for j in range(4):
				bo_sc = 0
				for k in range(i*4,i*4 + 4):
					cx,co = 0,0
					for l in range(j*4,j*4 + 4):
						cx,co = cx + board[k][l].count('x'), co + board[k][l].count('o')
					# print "hello"
					if co == 0:
						bo_sc += bo_ut[cx]
					else :
						bo_sc += 0
					if cx == 0:
						bo_sc -= bo_ut[co]
					else:
						bo_sc -= 0
					final = max(final, bo_sc)		
				# print "Y1"
				for k in range(j*4,j*4 + 4):
					cx,co = 0,0
					for l in range(i*4 ,i*4 + 4):
						cx,co = cx + board[l][k].count('x'), co + board[l][k].count('o')

					if co == 0:
						bo_sc += bo_ut[cx]
					else :
						bo_sc += 0
					if cx == 0:
						bo_sc -= bo_ut[co]
					else:
						bo_sc -= 0

					final = max(final, bo_sc)		
				# print "Y2"

				cx = board[i*4][j*4].count('x') + board[i*4 + 1][j*4 + 1].count('x') + board[i*4 + 2][j*4 + 2].count('x') + board[i*4 + 3][j*4 + 3].count('x')		
				co = board[i*4][j*4].count('o') + board[i*4 + 1][j*4 + 1].count('o') + board[i*4 + 2][j*4 + 2].count('o') + board[i*4 + 3][j*4 + 3].count('o')		

				if co == 0:
					bo_sc += bo_ut[cx]
				else :
					bo_sc += 0
				if cx == 0:
					bo_sc -= bo_ut[co]
				else:
					bo_sc -= 0
				# print "Y3"

				final = max(final, bo_sc)		

				cx = board[i*4][j*4 + 3].count('x') + board[i*4 + 1][j*4 + 2].count('x') + board[i*4 + 2][j*4 + 1].count('x') + board[i*4 + 3][j*4].count('x')		
				co = board[i*4][j*4 + 3].count('o') + board[i*4 + 1][j*4 + 2].count('o') + board[i*4 + 2][j*4 + 1].count('o') + board[i*4 + 3][j*4].count('o')		

				if co == 0:
					bo_sc += bo_ut[cx]
				else :
					bo_sc += 0
				if cx == 0:
					bo_sc -= bo_ut[co]
				else:
					bo_sc -= 0

				final = max(final, bo_sc)		
				# print "Y4", final
	

				temp[i].append(bo_sc)		

		rt = 0
		mult = 1

		for i in range(4):
			ans = 0
			for j in range(4):
				ans += temp[i][j]
				if(temp[i][j] >= 15): mult += 1;

			ans *= mult
			rt += ans
		# print "val1", rt
		newTemp = zip(*temp)
		mult = 1
		for i in range(4):
			ans = 0
			for j in range(4):
				ans += newTemp[i][j]
				if(temp[i][j] >= 15): mult += 1;

			x = newTemp[i].count(0)
			ans *= mult
			rt += (ans)
		# print "val2", rt

		#print temp

		ans = (temp[0][0] + temp[1][1] + temp[2][2] + temp[3][3])
		ans *= (4 - (1 if temp[0][0] < 15 else 0) - (1 if temp[1][1] < 15 else 0) - (1 if temp[2][2] < 15 else 0) - (1 if temp[3][3] < 15 else 0))

		rt += ans

		ans = (temp[0][3] + temp[1][2] + temp[2][1] + temp[3][0])
		ans *= (4 - (1 if temp[0][3] < 15 else 0) - (1 if temp[2][1] < 15 else 0) - (1 if temp[1][2] < 15 else 0) - (1 if temp[3][0] < 15 else 0))

		rt += ans

		return rt


	def calculate_utility_block(self,board,old_move,player,block, flag):
		self.ccc += 1
		bl_ut=[]
		if player=='x': 
			bl_ut = self.bl_ut
		else: 
			for i in self.bl_ut: 
				bl_ut.append(-i)
		bl_sc = 0
		#for utility of board status:
		#for rows:
		# print 'Block array is :' 
		# for i in range(4):
		# 	for j in range(4):
		# 		print block[i][j],
		# 	print 
		for i in range(4):
			countx = block[i].count('x');
			counto = block[i].count('o');
			if counto == 0: 
				bl_sc += bl_ut[countx];
			else:
				bl_sc += 0;
			if countx == 0: 
				bl_sc -= bl_ut[counto];
			else:
				bl_sc -= 0
		#for clm
		trArr = zip(*block)
		for i in range(4):
			countx = trArr[i].count('x');
			counto = trArr[i].count('o');
			if counto == 0: 
				bl_sc += bl_ut[countx];
			else:
				bl_sc += 0;
			if countx == 0: 
				bl_sc -= bl_ut[counto];
			else:
				bl_sc -= 0
		#for diagonal
		countx = block[0][0].count('x') + block[1][1].count('x') + block[3][3].count('x') + block[2][2].count('x')
		counto = block[0][0].count('o') + block[1][1].count('o') + block[3][3].count('o') + block[2][2].count('o')
		if counto == 0: 
			bl_sc += bl_ut[countx];
		else:
			bl_sc += 0;
		if countx == 0: 
			bl_sc -= bl_ut[counto];
		else:
			bl_sc -= 0
		#print
		countx = block[0][3].count('x') + block[1][2].count('x') + block[3][0].count('x') + block[2][1].count('x')
		counto = block[0][3].count('o') + block[1][2].count('o') + block[3][0].count('o') + block[2][1].count('o')
		if counto == 0: 
			bl_sc += bl_ut[countx];
		else:
			bl_sc += 0;
		if countx == 0: 
			bl_sc -= bl_ut[counto];
		else:
			bl_sc -= 0


		d = self.calculate_utility_board(board,old_move,player,block, flag)
		# print "hello dfsdfa", self.ccc
		# if bl_sc != 0: print 'ok bhai chal rha h ', bl_sc
		return ((bl_sc)**15) + d




		# when block is conquered


	def update2(self, old_move, new_move, block, board, player):

		x,y = new_move[0]/4, new_move[1]/4
		
		for i in range(4):
			if board[4*x + i][4*y + 1] == board[4*x + i][4*y + 2] == board[4*x + i][4*y + 3] == board[4*x + i][4*y] == player:
				block[x][y] = player
			if board[4*x + 1][4*y + i] == board[4*x + 2][4*y + i] == board[4*x + 3][4*y + i] == board[4*x][4*y + i] == player:
				block[x][y] = player

		if board[4*x][4*y] == board[4*x + 1][4*y + 1] == board[4*x + 2][4*y + 2] == board[4*x + 3][4*y + 3] == player:
			block[x][y] = player			
		if board[4*x][4*y + 3] == board[4*x + 1][4*y + 2] == board[4*x + 2][4*y + 3] == board[4*x + 3][4*y] == player:
			block[x][y] = player			

		for i in range(4):
			for j in range(4):
				if board[4*x + i][4*y + j] == '-':
					return block

		block[x][y] = 'd'
		return block


	def callMinMax(self,board,old_move,isMax,current_depth,player,Palpha,Pbeta,block,objBoard):

		validMoves = []
		if isMax: 
			best = -103
		else: 
			best = 103

		alpha = -10**(1000)
		beta = 10**(1000)

		x, y, flag1=(old_move[0]%4)*4,(old_move[1]%4)*4,0
	
		# if temp_status == 150 : print 'Hi',temp_status
		# if temp_status != 0: 
		# 	return temp_status

		if ((current_depth == self.maxDepth) or ((time.time() - self.start_time) > 14.5)): 
			# print old_move
			# for i in range(16):
			# 	for j in range(16):
			# 		print board[i][j], 
			# 		if j%4 == 3: print ' ', 
			# 	print 

			# print self.calculate_utility_block(board,old_move,player,block,0)
			return self.calculate_utility_block(board,old_move,player,block,0)


		for i in range(4):
			for j in range(4):
				if board[x+i][y+j] == '-' and block[(x+i)/4][(y+j)/4] == '-':
					validMoves.append([x+i,y+j])

		
		if isMax:

			if len(validMoves) == 0:
				# print "yolo2"
				
				newValid = self.generate_random_cells(objBoard)
				#random.shuffle(newValid)

				m1 = -10**12
				
				# print 'New valid = ', newValid
				
				for i,j in newValid:
					board[i][j] = player

					copiedBoard = copy.deepcopy(block)
					block = self.update2(old_move,[i,j], block, board, player)


					# change block
					
					m1 = max(m1, self.calculate_utility_block(board,[i,j],player,block,0))


					board[i][j] = '-'

					block = copy.deepcopy(copiedBoard)

					# change block

				return m1 

			for i,j in validMoves:
				board[i][j] = player
				copiedBoard = copy.deepcopy(block)
				# self.update2()
				block = self.update2(old_move,[i,j], block, board, player)

				# change block

				beta = Pbeta
				if alpha < beta:
					best = self.callMinMax(board,[i,j],not isMax, current_depth + 1, player, alpha, beta,block,objBoard)
					# print 'H value = ', best

					if alpha < best:
						alpha = best
					board[i][j] = '-'

					block = copy.deepcopy(copiedBoard)
					# change block

				else:
					board[i][j] = '-'
					block = copy.deepcopy(copiedBoard)
					# change block

					# print "chomu"
					break
			return alpha

		else:

			if len(validMoves) == 0:
				# print "yolo"
				newValid = self.generate_random_cells(objBoard)
				#random.shuffle(newValid)


				m1 = 10**12
				for i,j in newValid:
					if player == 'x': board[i][j] = 'o'
					else: board[i][j] = 'x'
					copiedBoard = copy.deepcopy(block)
					# self.update2()
					block = self.update2(old_move,[i,j], block, board, board[i][j])

					# change block
		
					m1 = min(m1, self.calculate_utility_block(board,[i,j],player,block,0))

					board[i][j] = '-'
					block = copy.deepcopy(copiedBoard)
					# change block


				return m1 
				# return 2

			
			for i,j in validMoves:
				if player == 'x': board[i][j] = 'o'
				else: board[i][j] = 'x'
				copiedBoard = copy.deepcopy(block)
				# self.update2()
				block = self.update2(old_move,[i,j], block, board, board[i][j])

				# change block

				alpha = Palpha
				if alpha < beta:
					# print 'H value = ', best

					best = self.callMinMax(board,[i,j],not isMax, current_depth + 1, player, alpha, beta,block,objBoard)
					if beta > best:
						beta = best
					board[i][j] = '-'
					block = copy.deepcopy(copiedBoard)
					# change block

				else:
					# print "chomu"

					board[i][j] = '-'
					block = copy.deepcopy(copiedBoard)
					# change block
					break
			return beta


	def find_valid_move_cells(self,board,old_move,player):
				

		# First move when old_move is initialised to [-1,-1]

		# if old_move[0] == old_move[1] == -1:
		# 	return 1,1
		# 	moves = self.generate_random_cells(board)

		# Condition if the whole board is filled or the block in which the player is to move is occupied
		# print "sdoihfiada"
		if self.block_occupied(board,old_move,player) == 0:
			moves = self.find_valid_cells(board,old_move)

		# Condition when the cell is full or captured
		else:
			moves = self.generate_random_cells(board)
			#random.shuffle(moves)


		# print 'hello = ', self.block_occupied(board.board_status,old_move,player)
		
		# print 'MOves = ', moves

		heuristic = -10**1003
		MIN = -10**1004
		MAX = 10**1004
		isMax = 0

		for i in range(len(moves)):
			x,y = moves[i][0],moves[i][1]
			board.board_status[x][y] = player

			# change block

			copiedBoard = copy.deepcopy(board.block_status)
			board.block_status =  self.update2(old_move, [x,y], board.block_status, board.board_status , player)

			cell = [x,y]
			temp = self.callMinMax(board.board_status,cell,isMax,0,player,MIN,MAX,board.block_status,board)
			if temp > heuristic:
				heuristic = temp
				f,g = x,y
			board.board_status[x][y] = '-'

			board.block_status = copy.deepcopy(copiedBoard)
			# change block


		# print 'Returning = ', f, g
		
		return f,g


	def move(self, board, old_move, flag):
		if(old_move == (-1,-1)):
			#print "yolo"
			return (5,5)
		self.start_time = time.time()
		self.maxDepth = 0
		final_move = (0,0)
		cells = (0,0)
		#print " hello"
		while ((time.time() - self.start_time)<14):
			#print "start time: ", self.start_time
			final_move = cells
			self.maxDepth += 1
			cells = self.find_valid_move_cells(board,old_move,flag)
			# print "depth", self.maxDepth

		return final_move