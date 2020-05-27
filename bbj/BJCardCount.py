# This file is part of Benevolent Blackjack.
# Copyright 2010 Philip M. White
# 
# Benevolent Blackjack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Benevolent Blackjack is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

from bbj.BJException import *
from bbj.Card import Card

strategylist = [
	# name		[ 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A]
	['ko',		[ 1, 1, 1, 1, 1, 1, 0, 0, -1,-1,-1,-1,-1]],
	['hi-lo',	[ 1, 1, 1, 1, 1, 0, 0, 0, -1,-1,-1,-1,-1]],
	['zen',		[ 1, 1, 2, 2, 2, 1, 0, 0, -2,-2,-2,-2,-1]],
]

# isStrategyKnown returns true if the given string refers to one of the
# strategies in 'strategylist'.
# Preconditions:
#  - arg 'name' is a string
# Postconditions:
#  - a boolean value is returned
def isStrategyKnown(name):
	for strategy in strategylist:
		if strategy[0] == name:
			return True
	return False

# rankindex returns the index of a given card in the vector of points of
# a strategy.
# Preconditions:
# - arg 'card' is a Card
# Postconditions:
# - an integer value is returned
# - the returned value addresses a value in any strategy point vector
def rankindex(card):
	return card.rank - Card.R_2

# Instances of BJCardCount hold the card-count state for a given strategy.
# During gameplay, BJCardCount instances receive new cards to count.
# At any point, a caller can query a BJCardCount instance about the current
# count.
class BJCardCount:
	def __init__(self, strategyName=None):
		self.strategy = None
		if strategyName is not None:
			for s in strategylist:
				if s[0] == strategyName:
					self.strategy = s
			if self.strategy is None:
				raise BJException("The requested card-counting strategy is unrecognized.")
		self.reset()

	def add(self, card):
		if self.strategy is None:
			return
		self.__count += self.strategy[1][rankindex(card)]

	def get(self):
		return self.__count

	def reset(self):
		self.__count = 0

	def isEnabled(self):
		return self.strategy is not None

	def __str__(self):
		if self.strategy is None:
			return "not enabled"
		return self.strategy[0]
