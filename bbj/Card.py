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

import codecs
import copy
import sys

from bbj.peafowlterm import *

class CardException(BaseException):
	pass

# Card instances are the individual cards.
# Each card has a suit and a rank.
# Each card also knows its string representation for terminal output.
class Card:
	# Suits
	Suit_Cl = 0
	Suit_Di = 1
	Suit_He = 2
	Suit_Sp = 3
	# Ranks
	R_2 = 2
	R_3 = 3
	R_4 = 4
	R_5 = 5
	R_6 = 6
	R_7 = 7
	R_8 = 8
	R_9 = 9
	R_10 = 10
	R_Ja = 11
	R_Qu = 12
	R_Ki = 13
	R_Ac = 14

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.setStrings()

	def setStrings(self):
		# Colors with 'bold' enabled appear to not display the card suits
		# in some environments, replacing the correct Unicode symbol with
		# a hollow rectangle.  To be safe, use non-bold colors.
		blackSuitColor = ColorScheme(ColorNavy, ColorGray)
		redSuitColor = ColorScheme(ColorBrown, ColorBrown)
		stream = sys.stdout
		if self.suit == self.Suit_Cl:
			suit = ColoredString("\u2663", blackSuitColor, stream)
		elif self.suit == self.Suit_Di:
			suit = ColoredString("\u2666", redSuitColor, stream)
		elif self.suit == self.Suit_He:
			suit = ColoredString("\u2665", redSuitColor, stream)
		elif self.suit == self.Suit_Sp:
			suit = ColoredString("\u2660", blackSuitColor, stream)
		else:
			raise CardException("A card has an unknown suit.")

		if self.rank >= self.R_2 and self.rank <= self.R_10:
			rank = str(self.rank)
		elif self.rank == self.R_Ja:
			rank = "J"
		elif self.rank == self.R_Qu:
			rank = "Q"
		elif self.rank == self.R_Ki:
			rank = "K"
		elif self.rank == self.R_Ac:
			rank = "A"
		else:
			raise CardException("A card has an unknown rank.")

		self.__strRepr = ColoredText(suit) + ColoredString(rank, stream=stream)

	def display(self):
		self.__strRepr.display()

	def getStrRepr(self):
		return self.__strRepr
