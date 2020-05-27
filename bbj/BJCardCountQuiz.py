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

# closestBelow finds the index of the element in 'list' closest to 'v' such
# that the element is smaller or equal to 'v'.
# This function could use a binary search, but I expect that 'list' will
# always be too small to warrant the larger code and higher overhead of a
# binary search algorithm.
# Preconditions:
# - arg 'list' is a list having at least one element
# - all elements in 'list' have the same type
# - values in 'list' are monotonically non-decreasing
# - arg 'v' has the same type as elements in 'list'
# Postconditions:
# - if there is an element of 'list' that matches the requirements,
#    its index is returned.  Otherwise, -1 is returned.
def closestBelow(list, v):
	if len(list) == 0:
		raise BJException("received an empty list")
	if list[0] > v:
		raise BJException("no element that meets criteria")
	for i in range(len(list)):
		if list[i] > v:
			return i-1
	return len(list)-1

# Instances of BJCardCountQuiz hold the state for the intermittent quizzes
# on card-counting that the player can choose to receive.  The state includes
# the amounts the player was off by.
class BJCardCountQuiz:
	def __init__(self):
		self.guessOffsetList = []
		self.guessOffsetIntervalList = []

	def guessMake(self, valueGuessed, valueActual):
		diff = valueGuessed - valueActual
		self.guessOffsetList.append(diff)
		self.guessOffsetIntervalList.append(diff)

	def intervalClear(self):
		self.guessOffsetIntervalList = []

	def intervalGetOffsets(self):
		return self.guessOffsetIntervalList

	def guessGetQuantity(self):
		return len(self.guessOffsetList)

	def guessGetGroup(self, grouping):
		# make stats the same size as grouping, but filled with zeros
		stats = map(lambda x: 0, grouping)
		for offset in self.guessOffsetList:
			idx = closestBelow(grouping, offset)
			stats[idx] += 1
		return stats
