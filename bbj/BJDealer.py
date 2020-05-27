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

import time

from bbj.BJException import *

Female = 0
Male = 1

# An instance of BJDealer is the dealer.  The instance knows its gender, has
# the shoe of cards, knows how slow to be, when to reshuffle, etc.
class BJDealer:
	def __init__(self, gender, shoe, reshuffleThresh, delay):
		self.gender = gender
		if self.gender != Male and self.gender != Female:
			raise BJException("The dealer's gender must be male or female.")
		self.shoe = shoe
		self.reshuffleThresh = reshuffleThresh
		self.delay = delay

	def shouldReshuffle(self):
		return self.shoe.numCardsRemaining() <= self.reshuffleThresh

	def reshuffleShoe(self):
		self.shoe.recreate()

	def getCard(self):
		return self.shoe.drawRnd()

	def getPronounPossessive(self):
		return "his" if self.gender == Male else "her"

	def getPronounSubjective(self):
		return "he" if self.gender == Male else "she"

	def getPronounObject(self):
		return "him" if self.gender == Male else "her"

	def pause(self):
		time.sleep(self.delay)
