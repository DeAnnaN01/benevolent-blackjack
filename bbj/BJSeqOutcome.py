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

GenericLost = -5
Surrender = -2
Bust = -1
Unsure = 0
Push = 1
BJ = 2
FCC = 3

# An instance of BJSeqOutcome holds the outcome of a sequence.
# The term "sequence" is defined in doc/.
class BJSeqOutcome:
	def __init__(self, outcome, bet, payoutMultiplier, cardsPlayed, score=-999):
		self.outcome = outcome
		self.bet = bet
		self.payoutMultiplier = payoutMultiplier
		self.cardsPlayed = cardsPlayed
		self.score = score
