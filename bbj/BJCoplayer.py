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

import BJPlayerAction
import BJStrategy

# Instances of BJCoplayer hold the state and make decisions for the coplayers
# sitting at the table.
class BJCoplayer:
	firstUnusedCharacter = 'A'
	def __init__(self):
		self.ID = self.firstUnusedCharacter
		self.__class__.firstUnusedCharacter = chr(ord(self.firstUnusedCharacter)+1)
		self.cards = []

	def reset(self):
		self.cards = []

	def takeCards(self, cards):
		self.cards += cards
		self.score = BJStrategy.getBestScore(self.cards)

	def getAction(self, card_dealer):
		if self.score >= 17:
			return BJPlayerAction.Stand
		elif self.score == 16 and BJStrategy.getHardValue(card_dealer) >= 9:
			return BJPlayerAction.Surrender
		elif self.score == 15 and BJStrategy.getHardValue(card_dealer) == 10:
			return BJPlayerAction.Surrender
		elif self.score > 13:
			if BJStrategy.getSoftValue(card_dealer) >= 7:
				return BJPlayerAction.Hit
			else:
				return BJPlayerAction.Stand
		elif self.score > 9 and len(self.cards) == 2:
				return BJPlayerAction.Double
		else:
			return BJPlayerAction.Hit

	def __str__(self):
		return self.ID
