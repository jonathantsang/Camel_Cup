# camels.py

import collections
import random

class CamelStack():
	def __init__(self):
		self.stack = collections.deque() # deque of camel ids

class Game():
	def __init__(self, boardsize):
		self.camelcount = 5 # Const
		self.players = {} # Key: player id, Value: score 0,1,2,3,4, etc.

		self.boardsize = boardsize
		self.board = [[str(i)] for i in range(0, boardsize+4)]

		self.camelarray = ['b', 'r', 'g', 'w', 'y'] # Camels 0,1,2,3,4
		self.camelspos = {} # Key: camel id (0,1,2,3,4), Value: position in the board

		# Bet cards for end of leg currency
		self.bets = {} # Key: player id, Value: Array of (Camel id, 1,2,3) pertaining to 1st,2nd,3rd bet on that camel

		# (camel id, player id)
		self.winnerguesses = [] # Front first
		self.loserguesses = [] # Front first
		
		self.dicedone = {} # Key: camel id, Value: true or false for rolled yet

		self.won = False
		print(self.board)

		self.Setup()

	# Check validity of the command given
	def Valid(self, inp):
		if inp == "":
			return False
		parsed = inp.split()
		if parsed[0] != 'r' and parsed[0] != 'pt' and parsed[0] != 'vl' and parsed[0] != 'vw' and parsed[0] != 'vc':
			return False
		elif (parsed[0] == 'pt' or parsed[0] == 'vl' or parsed[0] == 'vw' or parsed[0] == 'vc'):
			if len(parsed) == 1:
				return False
			elif (parsed[1] == 1 or parsed[1] == 2 or parsed[1] == 3 or parsed[1] == 4 or parsed[1] == 5):
				return False
		return True

	def Setup(self):
		print("Players")
		self.numplayers = int(input())
		for i in range(0, self.numplayers):
			print("Player " + str(i))
			self.players[i] = 0
		self.StartGame()

	def StartGame(self):
		# Initialize camels
		# B, R, G, W, Y
		print("Camels are: B(lue), R(ed), G(reen), W(hite), Y(ellow)")
		print(self.camelarray)

		for i, camel in enumerate(self.camelarray):
			self.camelspos[i] = 0
			pos = random.randint(0, 2)
			self.MoveCamel(i, pos, 1)

		self.PrintBoard()

		while(not self.won):
			i = 0
			while(i < self.numplayers):
				# Player i+1
				print("Player " + str(i) + "'s Turn:")

				inp = input()
				while not self.Valid(inp):
					print("ERROR in command")
					print("Valid Turn Commands: \nRoll -> r\nPlace Trap -> pt 1-size\nVote Loser -> vl 1,2,3,4,5\nVote Winner -> vw 1,2,3,4,5\nVote on Camel -> vc 1,2,3,4,5")
					inp = input()
				print("command: " + inp)

				# Perform the action
				inp = inp.split()
				
				# Roll
				if inp[0] == 'r':
					# Give player 1 point
					self.players[i] += 1

					cameldice = random.randint(0,4)
					while cameldice in self.dicedone:
						cameldice = random.randint(0,4)

					# Camel id chosen
					movement = random.randint(1,3)
					print("camel " + self.camelarray[cameldice] + " moved " + str(movement))
					self.MoveCamel(cameldice, movement, 0)
					self.PrintBoard()

					self.dicedone[cameldice] = 1
					
					if len(self.dicedone) == self.camelcount:
						self.EndOfLeg()

					for c in self.camelspos:
						if self.camelspos[c] >= self.boardsize:
							print ("Camel " + str(self.camelarray[c]) + " won!")
							self.won = True

				# Place trap
				if inp[0] == 'pt':
					pass
				# Vote loser
				if inp[0] == 'vl':
					self.loserguesses.append((inp[1], i))
					pass

				# Vote winner
				if inp[0] == 'vw':
					self.winnerguesses.append((inp[1], i))
					pass

				# Vote camel
				if inp[0] == 'vc':
					
					pass

				i += 1

	# Prints the game board
	def PrintBoard(self):
		top = ""
		numbers = ""

		# Each "tile" is __ and a " " for spacing

		maxheight = 0

		# print(self.board)
		# Position of each one
		for c in self.board:
			maxheight = max(maxheight, len(c))

		# Print column-wise
		height = maxheight
		i = 0
		while height > 1: # 1 is the number in array
			row = ""
			for c in self.board:
				#print(c, i)
				if len(c) >= height:
					row += str(self.camelarray[c[-1-(len(c)-height)]]) + "  "
				else:
					row += "   " # 3 space empty
			print(row)
			height -= 1
			i += 1

		# Array of CamelStack on the self.board
		for i, b in enumerate(self.board):
			top += "__ "
			if i < 10:
				numbers += str(i) + "  "
			else:
				numbers += str(i) + " "
		print(top)
		print(numbers)

	def MoveCamel(self, camel, amt, start=0):
		camelidx = -1
		camelcomponent = [camel]

		if start != 1:
			# Remove from old position
			camelidx = self.board[self.camelspos[camel]].index(camel) # Everything beyond this is also moved
			camelcomponent = self.board[self.camelspos[camel]][camelidx:]
			self.board[self.camelspos[camel]] = self.board[self.camelspos[camel]][:camelidx] # cut off
		else:
			pass

		for c in camelcomponent:
			self.camelspos[c] += amt

		# Move to new position
		self.board[self.camelspos[camel]].extend(camelcomponent)

	# Prints position of game for AIs (can only see current player's information)
	def Position(self, player):
		pass

	# Scores of people human-readable
	def Scores(self):
		for player in self.players:
			print("Player: " + player)
			print("Score: " + self.players[player])

	# Once all camels have moved
	def EndOfLeg(self):
		print("EndofLeg")
		
		# Tally bets



		self.dicedone = {} # clear dice again

	# Vote loser and winner tallied
	def EndOfGame(self):
		print("EndofGame")
		pass
	# Check if move is possible:
	# voting on current camel isn't exhausted
	# placing a tile not beside another tile, or under current camels
	def CheckPossible(self, inp):
		pass

# Turn
# Roll -> r
# place trap -> pt 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 (still valid spot check)
# vote loser -> vl 1,2,3,4,5
# vote winner -> vw 1,2,3,4,5
# Winners/Losers, reverse order
# 8, 5, 3, 1
# Wrong are -1

# vote on camel -> vc 1,2,3,4,5
# Vote camel:
# First place, second, 3-5
# first to vote: 5, 1, -1 
# second to vote: 3, 1, -1

a = Game(20)