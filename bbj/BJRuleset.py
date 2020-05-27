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
from bbj.money import fmtMoney

# An instance of BJRuleset holds the set of rules for a Blackjack table.
class BJRuleset:
	def __init__(self,
			numDecks,
			tableMin,
			tableMax,
			reshuffleThreshold,
			blackjackPayout,
			allowDouble,
			allowSurrender,
			allowDAS,
			allowHitSplitAces,
			hitSoft17,
			fiveCardCharlie):
		self.numDecksSet(numDecks)
		self.tableMinSet(tableMin)
		self.tableMaxSet(tableMax)
		self.reshuffleThresholdSet(reshuffleThreshold)
		self.blackjackPayoutSet(blackjackPayout)
		self.allowDoubleSet(allowDouble)
		self.allowSurrenderSet(allowSurrender)
		self.allowDASSet(allowDAS)
		self.allowHitSplitAcesSet(allowHitSplitAces)
		self.hitSoft17Set(hitSoft17)
		self.fiveCardCharlieSet(fiveCardCharlie)

	def numDecksSet(self, v):
		if v < 1:
			raise BJException("The number of decks must be positive.")
		if v > 100:
			raise BJException("The number of decks must not be greater than 100.")
		self.numDecks = v

	def tableMinSet(self, v):
		if v < 0:
			raise BJException("The table minimum must be non-negative.")
		self.tableMin = v

	def tableMaxSet(self, v):
		if v < 0:
			raise BJException("The table maximum must be non-negative.")
		self.tableMax = v

	def blackjackPayoutSet(self, v):
		if not 'n' in v or not 'd' in v:
			raise BJException("The blackjack payout must be a ratio written as #:#.")
		if v['d'] == 0:
			raise BJException("Hitting Blackjack must not end the universe.")
		self.blackjackPayout = v

	def allowDoubleSet(self, v):
		self.allowDouble = v

	def allowSurrenderSet(self, v):
		self.allowSurrender = v

	def allowDASSet(self, v):
		self.allowDAS = v

	def allowHitSplitAcesSet(self, v):
		self.allowHitSplitAces = v
	def hitSoft17Set(self, v):
		self.hitSoft17 = v

	def fiveCardCharlieSet(self, v):
		self.fiveCardCharlie = v

	def reshuffleThresholdSet(self, v):
		self.reshuffleThreshold = v

	def __str__(self):
		msg = "== Table Rules ==\n"
		msg += ("\tNumber of decks:         %d\n" % self.numDecks)
		msg += ("\tTable minimum:           %s\n" % fmtMoney(self.tableMin))
		msg += ("\tTable maximum:           %s\n" % fmtMoney(self.tableMax))
		msg += ("\tReshuffle threshold:     %d cards remaining\n" % self.reshuffleThreshold)
		msg += ("\tBlackjack payout:        %d:%d\n" % (self.blackjackPayout['n'], self.blackjackPayout['d']))
		msg += ("\tAllow doubling:          %s\n" % ("yes" if self.allowDouble else "no"))
		msg += ("\tAllow surrender:         %s\n" % ("yes" if self.allowSurrender else "no"))
		msg += ("\tAllow DAS:               %s\n" % ("yes" if self.allowDAS else "no"))
		msg += ("\tAllow hit split aces:    %s\n" % ("yes" if self.allowHitSplitAces else "no"))
		msg += ("\tHit on soft 17:          %s\n" % ("yes" if self.hitSoft17 else "no"))
		msg += ("\tFive-card charlie:       %s\n" % ("enabled" if self.fiveCardCharlie else "not enabled"))
		return msg
