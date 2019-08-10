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

		# Traps
		self.traps = {} # Key: player id, Value: (+1 or -1, position in the board)

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

	def CalculatePayoff(self, order, camelorder):
		if camelorder <= 3:
			return -1
		elif camelorder == 2:
			return 1
		# Order is 0st, 1st, 2nd, etc.
		order += 1

		if order == 1:
			return 5
		else:
			return 3

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
			i = 0 # current player turn

			while(i < self.numplayers):
				# Player i+1
				print("Player " + str(i) + "'s Turn:")
				print("DEBUG")
				print("d -> debug")
				print("s -> human readable scores")
				print("m -> parseable data for AI")

				# Python 3
				inp = input()

				# DEBUG
				if inp[0] == 'd':
					self.Debug()
					continue
				elif inp[0] == 's':
					self.Scores()
					continue
				elif inp[0] == 'm':
					self.Data()

				while not self.Valid(inp):
					print("ERROR in command")
					print("Valid Turn Commands: \nRoll -> r\nPlace Trap -> pt 1-size\nVote Loser -> vl 1,2,3,4,5\nVote Winner -> vw 1,2,3,4,5\nVote on Camel -> vc 1,2,3,4,5")
					inp = input()
				print("command: " + inp)

				# Could fail, loop again
				if (not self.CheckPossible(inp, i)):
					print("Move is not possible. Please try again.")
					continue

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
						print("End of Leg")
						self.EndOfLeg()

					for c in self.camelspos:
						if self.camelspos[c] >= self.boardsize:
							print ("Camel " + str(self.camelarray[c]) + " won!")
							self.won = True

				# Place trap
				elif inp[0] == 'pt':
					# This can fail due to not valid trap space
					self.traps[i] = (int(inp[1]), int(inp[2]))					

				# Vote loser
				elif inp[0] == 'vl':
					camelid = int(self.camelarray.find(inp[1]))
					# This can fail if you don't own the card for voting winner/loser
					self.loserguesses.append((camelid, i))

				# Vote winner
				elif inp[0] == 'vw':
					int(self.camelarray.index(inp[1]))
					# This can fail if you don't own the card for voting winner/loser
					self.winnerguesses.append((camelid, i))

				# Vote camel
				elif inp[0] == 'vc':
					# This can fail if 2 players already voted for a camel
					if i not in self.bets:
						self.bets[i] = []

					# Find 1st, 2nd, 3rd
					camelid = int(self.camelarray.index(inp[1]))
					amt = 0

					for player_bets in self.bets:
						for bet in self.bets[player_bets]:
							if bet[0] == camelid:
								amt += 1

					self.bets[i].append((camelid, amt))

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

		# Check if it is a trap and move accordingly
		for player in self.traps:
			val = self.traps[player][0]
			position = self.traps[player][1]

			if position == self.camelspos[camel]: 
				# Credit player who placed the trap
				self.players[player] += 1

				# +1
				if val == 1:
					for c in camelcomponent:
						self.camelspos[c] += 1
					# Move to new position, appending to the ones there
					self.board[self.camelspos[camel]].extend(camelcomponent)
				elif val == -1:
					for c in camelcomponent:
						self.camelspos[c] -= 1
					# Move to new position, placing under the previous if there
					self.board[self.camelspos[camel]] = camelcomponent.extend(self.board[self.camelspos[camel]])
				break # No traps on traps

	# Prints position of game for AIs (can only see current player's information)
	def Position(self, player):
		print("Information for player" + str(player))
		print("Player " + str(player) + "has " + str(self.players[player]) + " points")

	# Debug for state of game currently
	def Debug(self):
		print("camelcount")
		print(self.camelcount)
		print("players")
		print(self.players)
		print("boardsize")
		print(self.boardsize)
		print("board")
		print(self.board)
		print("camelarray")
		print(self.camelarray)
		print("camelspos")
		print(self.camelspos)
		print("bets")
		print(self.bets)
		print("winnerguesses")
		print(self.winnerguesses)
		print("loserguesses")
		print(self.loserguesses)
		print("dicedone")
		print(self.dicedone)
		print("traps")
		print(self.traps)
		print("won")
		print(self.won)

	# Scores of people human-readable
	def Scores(self):
		for player in self.players:
			print("Player: " + str(player))
			print("Score: " + self.players[player])

	# Data for computers
	def Data(self):
		pass

	# Once all camels have moved
	def EndOfLeg(self):
		print("EndofLeg")

		# Find the camel orders
		camels = []
		for camel in self.camelspos:
			# (position, id)
			camels.append((camel[1], camel[0]))
		camels.sort()

		print("CAMEL PLACES")
		print(camels)

		camelpos = {} # Key: Camel id, Value: Camel position relative to others 1,2,3,4,5
		for i, camel in enumerate(camels):
			camelpos[i] = camel[0]

		# Update the scores
		for bet in self.bets:
			playerdid = bet
			camelid = self.bets[bet][0]
			orderofbet = bet[1]

			payoff = self.CalculatePayoff(orderofbet, camelpos[camelid])
			self.players[playerid] += payoff

		self.Scores()

		self.dicedone = {} # clear dice again

	# Vote loser and winner tallied
	def EndOfGame(self):
		print("EndofGame")
		pass

	# Check if move is possible:
	# voting on current camel isn't exhausted (2+ players)
	# placing a tile not beside another tile, or under current camels
	# if you don't own card to vote on winner/loser
	def CheckPossible(self, inp, playerid):
		if inp[0] == 'pt':
			# This can fail due to not valid trap space
			placed = int(inp[1])

			# If there is an adjacent trap, you cannot place it there
			for trap in self.traps:
				if (trap[1] - 1 == placed) or (trap[1] + 1 == placed):
					print("Invalid trap spot since it is adjacent to a trap on " + str(trap[1]))
					return False

		# Vote loser or Vote winner
		elif inp[0] == 'vl' or inp[0] == 'vw':
			# camel id to attempt to guess
			camelid = int(self.camelarray.index(inp[1])) # Search for id

			# This can fail if you don't own the card for voting winner/loser
			for guess in self.winnerguesses:
				if guess[1] == playerid and guess[0] == camelid:
					print("Player has already bet on a loser/winner with camelid")
					return False

			for guess in self.loserguesses:
				if guess[1] == playerid and guess[0] == camelid:
					print("Player has already bet on a loser/winner with camelid")
					return False

		# Vote camel
		elif inp[0] == 'vc':
			# This can fail if 2 players already voted for a camel
			camelid = int(self.camelarray.index(inp[1])) # Search for id
			amt = 0

			for player_bets in self.bets:
				for bet in player_bets[1]:
					if bet[0] == camelid:
						amt += 1

			if amt == 2:
				print("Camel already has 2 bettors")
				return False

		return True

# Turn
# Roll -> r
# vote on camel -> vc r, b, g, w, o
# place trap -> pt 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 (still valid spot check) 1 or -1
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
# no third

a = Game(20)