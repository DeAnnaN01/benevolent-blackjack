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

from bbj.CasinoComp import *

# The mathematical expectation for the casino as a decimal.
BJCasinoExpectation = 0.015

compList = [
	CasinoComp('a free buffet', 10),
	CasinoComp('a coupon for free room and food', 60),
	CasinoComp('a coupon for free room, food, and beverage', 70),
	CasinoComp('a free round-trip flight back to the casino', 150),
]

def chooseComp(roundsPlayed, minsPlayed, totalWagered):
	if roundsPlayed == 0 or minsPlayed == 0:	# to avoid divide-by-zero
		return None
	if minsPlayed < 30:
		return None
	roundsPerMinute = float(roundsPlayed) / minsPlayed
	avgBet = float(totalWagered) / roundsPlayed
	estimatedCasinoGain = roundsPlayed * avgBet * BJCasinoExpectation
	if roundsPerMinute < 1:
		return None
	for i in range(len(compList)-1, -1, -1):
		if estimatedCasinoGain >= compList[i].value:
			return compList[i]
	return None
