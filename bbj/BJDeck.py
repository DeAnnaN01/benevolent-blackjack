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

from bbj.Card import Card
from bbj.Deck import Deck

from bbj.BJException import *

numSuits = 4

# itersuit is an iterator over suits
# Preconditions: none
# Postconditions: none
def itersuit():
	for suit in [Card.Suit_Cl, Card.Suit_Di, Card.Suit_He, Card.Suit_Sp]:
		yield suit

# iterrank is an iterator over ranks
# Preconditions: none
# Postconditions: none
def iterrank():
	for rank in [Card.R_2, Card.R_3, Card.R_4, Card.R_5, Card.R_6, Card.R_7,
		Card.R_8, Card.R_9, Card.R_10, Card.R_Ja, Card.R_Qu, Card.R_Ki,
		Card.R_Ac]:
		yield rank

# An instance of BJDeck is a deck of cards for Blackjack.
class BJDeck(Deck):
	def __init__(self):
		Deck.__init__(self)
		numSuitsNow = 0
		for suit in itersuit():
			for rank in iterrank():
				self.cards.append(Card(suit, rank))
			numSuitsNow += 1
		if numSuits != numSuitsNow:
			raise BJException("Blackjack requires %d suits; instead we have %d." % (numSuits, numSuitsNow))
		self.shuffle()
