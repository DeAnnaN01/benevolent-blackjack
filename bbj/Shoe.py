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

import random

from bbj.Deck import Deck

class ShoeException(BaseException):
	pass

class Shoe:
	"""
	An instance of Shoe is a device that holds cards, usually shuffled.  This
	allows the dealer to draw individual cards precisely without manipulating the
	entire deck of cards in his hands.
	"""
	def __init__(self, numdecks, deckClass):
		if not issubclass(deckClass, Deck):
			raise ShoeException("Shoe must be instantiated with a subclass of Deck")
		self.numdecks = numdecks
		self.deckClass = deckClass
		self.recreate()

	def drawSeq(self):
		"""
		Draws the top card from from the first available deck.
		"""
		if self.numdecks == 0:
			raise ShoeException("The shoe is out of cards.")
		card = self.decks[0].draw()
		if self.decks[0].size() == 0:
			self.decks[0:1] = [] # remove this deck
			self.numdecks -= 1
		return card

	def drawRnd(self):
		"""
		Draws the top card from from a randomly-chosen deck.
		"""
		if self.numdecks == 0:
			raise ShoeException("The shoe is out of cards.")
		decknum = random.randint(0, self.numdecks-1)
		deck = self.decks[decknum]
		card = deck.draw()
		if deck.size() == 0:
			self.decks[decknum:decknum+1] = [] # remove this deck
			self.numdecks -= 1
		return card

	def recreate(self):
		self.decks = []
		for i in range(self.numdecks):
			deck = self.deckClass()
			self.decks.append(deck)

	def numCardsRemaining(self):
		num = 0
		for deck in self.decks:
			num += deck.size()
		return num

	def __str__(self):
		return "<Shoe of %s at %s; %d cards remain>" % (self.deckClass, id(self), self.numCardsRemaining())

