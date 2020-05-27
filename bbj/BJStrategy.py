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

from functools import reduce

from bbj.BJException import *
import bbj.BJPlayerAction
from bbj.Card import Card

H = 0	# hit
S = 1	# stand
Dh = 2	# double, else hit
Ds = 3	# double, else stand
P = 4	# split
U = 5	# surrender

# The following tables of basic strategy were taken from Wikipedia's
# article on "Blackjack" and combined with Richard A. Epstein's book
# "The Theory of Gambling and Statistical Logic," revised edition,
# page 227.
# The two sources disagree with each other in some situations, so I
# tried to combine them the best I could.

# Wikipedia's strategy tables are valid for when the dealer stands on
# soft 17.  If the program's ruleset hits on soft 17, this strategy
# is adjusted from what's hard-coded here.

hardTotals = [
	#2,  3,  4,  5,  6,  7,  8,  9, 10,  A		# dealer's upcard
	[S,  S,  S,  S,  S,  S,  S,  S,  S,  S],	# player has 20 points
	[S,  S,  S,  S,  S,  S,  S,  S,  S,  S],	# player has 19 points
	[S,  S,  S,  S,  S,  S,  S,  S,  S,  S],	# player has 18 points
	[S,  S,  S,  S,  S,  S,  S,  S,  S,  S],	# player has 17 points
	[S,  S,  S,  S,  S,  H,  H,  U,  U,  U],	# player has 16 points
	[S,  S,  S,  S,  S,  H,  H,  H,  U,  H],	# player has 15 points
	[S,  S,  S,  S,  S,  H,  H,  H,  H,  H],	# player has 14 points
	[S,  S,  S,  S,  S,  H,  H,  H,  H,  H],	# player has 13 points
	[H,  H,  S,  S,  S,  H,  H,  H,  H,  H],	# player has 12 points
	[Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, H],	# player has 11 points
	[Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, H,  H],	# player has 10 points
	[H,  Dh, Dh, Dh, Dh, Dh, H,  H,  H,  H],	# player has 9 points
	[H,  H,  H,  H,  Dh, H,  H,  H,  H,  H],	# player has 8 points
	[H,  H,  H,  H,  H,  H,  H,  H,  H,  H],	# player has 7 points
	[H,  H,  H,  H,  H,  H,  H,  H,  H,  H],	# player has 6 points
	[H,  H,  H,  H,  H,  H,  H,  H,  H,  H],	# player has 5 points
]

softTotals = [
	#2,  3,  4,  5,  6,  7,  8,  9, 10,  A		# dealer's upcard
	[S,  S,  S,  S,  S,  S,  S,  S,  S,  S],	# player has A,9
	[S,  S,  S,  S,  S,  S,  S,  S,  S,  S],	# player has A,8
	[S,  Ds, Ds, Ds, Ds, S,  S,  H,  H,  S],	# player has A,7
	[H,  Dh, Dh, Dh, Dh, H,  H,  H,  H,  H],	# player has A,6
	[H,  H,  Dh, Dh, Dh, H,  H,  H,  H,  H],	# player has A,5
	[H,  H,  Dh, Dh, Dh, H,  H,  H,  H,  H],	# player has A,4
	[H,  H,  H,  Dh, Dh, H,  H,  H,  H,  H],	# player has A,3
	[H,  H,  H,  Dh, Dh, H,  H,  H,  H,  H],	# player has A,2
]

pairs = [
	#2,  3,  4,  5,  6,  7,  8,  9, 10,  A		# dealer's upcard
	[P,  P,  P,  P,  P,  P,  P,  P,  P,  P],	# player has A,A
	[S,  S,  S,  S,  S,  S,  S,  S,  S,  S],	# player has 10,10
	[P,  P,  P,  P,  P,  S,  P,  P,  S,  S],	# player has 9,9
	[P,  P,  P,  P,  P,  P,  P,  P,  P,  P],	# player has 8,8
	[P,  P,  P,  P,  P,  P,  H,  H,  H,  H],	# player has 7,7
	[P,  P,  P,  P,  P,  H,  H,  H,  H,  H],	# player has 6,6
	[Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, H,  H],	# player has 5,5
	[H,  H,  H,  P,  P,  H,  H,  H,  H,  H],	# player has 4,4
	[P,  P,  P,  P,  P,  H,  H,  H,  H,  H],	# player has 3,3
	[P,  P,  P,  P,  P,  H,  H,  H,  H,  H],	# player has 2,2
]

# optimalFind finds the optimal action in any possible circumstance.
# Preconditions:
# - arg 'ruleset': a BJRuleset object
# - arg 'cards_mine': a list of Card objects
# - arg 'card_dealer': a Card object
# - the tables 'softTotals', 'hardTotals', and 'pairs' exist and are
#   of the expected structure
# Postconditions:
# - an action of type BJPlayerAction is returned, or an exception is raised
def optimalFind(ruleset, cards_mine, card_dealer):
	ideal = None
	total_mine = getBestScore(cards_mine)
	# Find the column in all matrices based on the dealer's card.
	if card_dealer.rank == Card.R_Ac:
		col = 9
	elif card_dealer.rank >= Card.R_10:
		col = 8
	else:
		col = card_dealer.rank - 2

	if len(cards_mine) == 2 and cards_mine[0].rank == cards_mine[1].rank:
		rank = cards_mine[0].rank
		if rank == Card.R_Ac:
			row = 0
		elif rank >= Card.R_10:
			row = 1
		else:
			row = 10 - rank + 1
		ideal = pairs[row][col]
	else:
		complement = getAceComplement(cards_mine)
		if complement is None:
			# there is no Ace in this hand
			row = 20 - total_mine
			ideal = hardTotals[row][col]
		else:
			row = 9 - complement.rank
			ideal = softTotals[row][col]

	# Do we need to make an adjustment?
	if ruleset.hitSoft17:
		complement = getAceComplement(cards_mine)
		if total_mine == 11 and card_dealer == Card.R_Ac:
			ideal = D
		elif complement == Card.R_7 and card_dealer == Card.R_2:
			ideal = D
		elif complement == Card.R_8 and card_dealer == Card.R_6:
			ideal = D

	if ideal == U and not ruleset.allowSurrender:
		ideal = H
	elif ideal == Dh and not ruleset.allowDouble:
		ideal = H
	elif ideal == Ds and not ruleset.allowDouble:
		ideal = S

	if ideal == H:
		return bbj.BJPlayerAction.Hit
	elif ideal == S:
		return bbj.BJPlayerAction.Stand
	elif ideal == Dh or ideal == Ds:
		return bbj.BJPlayerAction.Double
	elif ideal == P:
		return bbj.BJPlayerAction.Split
	elif ideal == U:
		return bbj.BJPlayerAction.Surrender
	raise BJException("Could not find a proper action to return!")

# getHardValue returns the value of any card, treating an Ace as 11 points.
# Preconditions:
# - arg 'card': a Card object
# Postconditions:
# - an integer value is returned
def getHardValue(card):
	if card.rank <= Card.R_10:
		return card.rank
	if card.rank == Card.R_Ac:
		return 11
	return 10

# getSoftValue returns the value of any card, treating an Ace as 1 point.
# Preconditions:
# - arg 'card': a Card object
# - getHardValue() returns a correct value for at least all cards except an Ace
# Postconditions:
# - an integer value is returned
def getSoftValue(card):
	if card.rank == Card.R_Ac:
		return 1
	return getHardValue(card)

# getMaxScore returns the maximum score that a hand is worth.
# Preconditions:
# - arg 'cards': a list of Card objects
# Postconditions:
# - an integer value is returned
def getMaxScore(cards):
	totalH = 0
	for c in cards:
		totalH += getHardValue(c)
	return totalH

# getMinScore returns the minimum score that a hand is worth.
# Preconditions:
# - arg 'cards': a list of Card objects
# Postconditions:
# - an integer value is returned
def getMinScore(cards):
	totalS = 0
	for c in cards:
		totalS += getSoftValue(c)
	return totalS

# getBestScore returns the best score that a hand is worth, where "best" is
# as close to 21 as possible without going over.
# The algorithm is:
# 1) get the maximum score the hand is worth;
# 2) if the maximum score is 21 or below, this is the best score;
# 3) otherwise, as long as the score is above 21 and there are 11-valued
#    Aces in the hand, change the value of an Ace from 11 to 1;
# 4) return the score either when we reach to 21 or below, or when there
#    remain no more 11-valued Aces.
# Preconditions:
# - arg 'cards': a list of Card objects
# - arg 'maxScore': an integer
# Postconditions:
# an integer value is returned
def getBestScore(cards, maxScore=21):
	total = getMaxScore(cards)
	if total <= maxScore:
		return total
	values = []
	total = 0
	for c in cards:
		v = getHardValue(c)
		values.append(v)
		total += v
	haveAces = True
	while haveAces and total > maxScore:
		haveAces = False
		for i in range(len(values)):
			if values[i] == 11:
				values[i] = 1
				haveAces = True
				break
		total = reduce((lambda x,y: x+y), values)
	return total

# getAceComplement returns the other card in a two-card hand that has an Ace.
# Preconditions:
# - arg 'cards': a list of Card objects
# Postconditions:
# - returns a Card object or None
def getAceComplement(cards):
	if len(cards) != 2:
		# no pair
		return None
	if cards[0].rank == Card.R_Ac:
		return cards[1]
	if cards[1].rank == Card.R_Ac:
		return cards[0]
	# no Ace
	return None
	
