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

import bbj.BJPlayerAction
from bbj.BJRoundOutcome import BJRoundOutcome
import bbj.BJSeqOutcome
import bbj.BJStrategy
from bbj.Card import Card
from bbj.Purse import PurseException
from bbj.money import fmtMoney
from bbj.peafowlterm import *

# iPrint writes a message to a stream and indents is by a certain amount.
# Preconditions:
# - arg 'msg': a ColoredString object
# - arg 'stream': a stream such as sys.stdout
# - arg 'indent': an integer
# Postconditions:
# - stream is written to
def iPrint(msg, stream, indent):
	spc = ""
	# create 'indent' number of spaces
	spc += reduce(lambda x,y: x+y, map(lambda x: ' ', range(indent)), '')
	stream.write(spc)
	msg.display()
	stream.flush()

# playerGetAction asks the user for his desired action.
# Preconditions:
# - arg 'ruleset': an instance of BJRuleset
# - arg 'indent': an integer
# - arg 'can_split': a boolean
# Postconditions:
# - a member of BJPlayerAction is returned
def playerGetAction(ruleset, indent, can_split):
	def makeColoredAction(actionTuple):
		actionKeyColor = ColorScheme(ColorYellow, ColorOrange)
		tmpStr = ColoredText(ColoredString(actionTuple[0][0:actionTuple[1]])) + \
			ColoredString(actionTuple[0][actionTuple[1]], actionKeyColor) + \
			ColoredString(actionTuple[0][actionTuple[1]+1:])
		return tmpStr

	def findActionMatch(allowedActions, input):
		input = input.strip()
		if len(input) != 1:
			return None
		for aa in allowedActions:
			if input == aa[0][aa[1]]:
				return aa[2]
		return None

	allowedActions = [
		('hit', 0, bbj.BJPlayerAction.Hit),
		('stand', 0, bbj.BJPlayerAction.Stand),
	]
	if can_split:
		allowedActions.append(('split', 1, bbj.BJPlayerAction.Split))
	if ruleset.allowDouble:
		allowedActions.append(('double', 0, bbj.BJPlayerAction.Double))
	if ruleset.allowSurrender:
		allowedActions.append(('surrender', 1, bbj.BJPlayerAction.Surrender))
	actionMsg = ColoredText(ColoredString("You can "))
	for i in range(len(allowedActions)):
		actionTuple = allowedActions[i]
		if i < len(allowedActions)-1:
			tmpStr = makeColoredAction(actionTuple) + ColoredString(", ")
			actionMsg.append(tmpStr)
		else:
			actionMsg.append(ColoredText(ColoredString("or ")) + \
									makeColoredAction(actionTuple))
	actionMsg.append(ColoredString(": "))
	while True:
		iPrint(actionMsg, sys.stdout, indent)
		action = findActionMatch(allowedActions, sys.stdin.readline())
		if action is None:
			iPrint(ColoredString("You did not enter a valid option.\n", stream=sys.stderr), sys.stderr, indent)
		else:
			return action

# playerGetInsuranceDecision determines whether the player wants to buy
# insurance, and if so, then for how much.
# Preconditions:
# - arg 'maxBet': a positive integer
# Postconditions:
# - an amount between [1, maxBet] is returned, or None if the player does not want insurance
def playerGetInsuranceDecision(maxBet):
	indent = 0
	insuranceColor = ColorScheme(ColorLime, ColorGreen)
	if maxBet < 1:
		return None
	insYN = None
	while insYN is None:
		insString = ColoredText(ColoredString("Would you like to buy ")) + \
			ColoredString("insurance", insuranceColor) + \
			ColoredString("? (y/n): ")
		iPrint(insString, sys.stdout, indent)
		response = sys.stdin.readline().strip()
		if response == 'y':
			insYN = True
		elif response == 'n':
			insYN = False
		else:
			iPrint(ColoredString("You did not enter a valid option.\n", stream=sys.stderr), sys.stderr, indent)
	insAmount = None
	if not insYN:
		return insAmount
	while insAmount is None:
		iPrint(ColoredString("How much to bet for insurance? (Max: %s) $" % fmtMoney(maxBet)), sys.stdout, indent)
		try:
			amt = int(sys.stdin.readline().strip())
		except ValueError as e:
			sys.stderr.write("Error: you must enter an integer.\n")
			continue
		if amt > maxBet:
			iPrint(ColoredString("Your insurance bet must be at most %s.\n" % fmtMoney(maxBet), stream=sys.stderr), sys.stderr, indent)
		elif amt < 1:
			iPrint(ColoredString("Your insurance bet must be at least %s.\n" % fmtMoney(1), stream=sys.stderr), sys.stderr, indent)
		else:
			insAmount = amt
	return insAmount

# playerGetBet asks the user how much to bet.
# Preconditions:
# - arg 'purse': an instance of Purse
# - arg 'betMin': an integer
# - arg 'betMax': an integer
# - betMin <= betMax
# Postconditions:
# - bet is returned
def playerGetBet(purse, betMin, betMax):
	gotBet = False
	while not gotBet:
		sys.stdout.write("Your balance: %s.  Your bet: $" % purse)
		sys.stdout.flush()
		try:
			amt = int(sys.stdin.readline().strip())
		except ValueError as e:
			sys.stderr.write("Error: you must enter an integer.\n")
			continue
		if amt < betMin:
			print("The table minimum is %s." % betMin)
			continue
		if amt > betMax:
			print("The table maximum is %s." % betMax)
			continue
		try:
			purse.reserve(amt)
			gotBet = True
		except PurseException as e:
			sys.stderr.write("Error: %s\n" % e)
	return amt

# blackjack determines whether the given cards have a blackjack.
# Preconditions:
# - arg 'cards': a list of Card objects
# Postconditions:
# - returns True if have a blackjack; else returns False
def blackjack(cards):
	if len(cards) != 2:
		return False
	return (bbj.BJStrategy.getHardValue(cards[0]) == 11 and bbj.BJStrategy.getHardValue(cards[1]) == 10) or \
		(bbj.BJStrategy.getHardValue(cards[1]) == 11 and bbj.BJStrategy.getHardValue(cards[0]) == 10)

# bust determines whether the given cards go over 21 points.
# Preconditions:
# - arg 'cards': a list of Card objects
# Postconditions:
# - returns True if minimum score is over 21; else False
def bust(cards):
	return bbj.BJStrategy.getMinScore(cards) > 21

# playSequence plays a sequence of the main player.  ("Sequence" is defined in doc/.)
# Preconditions:
# - arg 'ruleset': an instance of BJRuleset
# - arg 'dealer': an instance of BJDealer
# - arg 'purse': an instance of BJPurse
# - arg 'cards_mine': a list of Card objects
# - arg 'card_dealer': an instance of Card
# - arg 'bet': a float
# - arg 'can_split': boolean
# - cards_mine has at least two elements
# - card_dealer is the face-up card of the dealer
# - bet must be already reserved in the purse
# Postconditions:
# - dealer and  purse are affected
# - a list of BJSeqOutcome objects is returned, one for each sequence played
def playSequence(settings, dealer, purse, cards_mine, card_dealer, bet, indent, can_split):
	outcome = None
	strategyIsGood = True
	payoutMultiplier = 1

	yourCardsDisplay = ColoredText(ColoredString("You: "))
	yourCardsDisplay += cards_mine[0].getStrRepr()
	yourCardsDisplay += ColoredString(" and ")
	yourCardsDisplay += cards_mine[1].getStrRepr()
	yourCardsDisplay += ColoredString(".\n")
	iPrint(yourCardsDisplay, sys.stdout, indent)
	if blackjack(cards_mine):
		outcome = bbj.BJSeqOutcome.BJ
		payoutMultiplier = float(settings['ruleset'].blackjackPayout['n']) / settings['ruleset'].blackjackPayout['d']
	# If we split on aces, do not allow the user any further actions.
	if not can_split and cards_mine[0] == Card.R_Ac and not settings['ruleset'].allowHitSplitAces:
		outcome = bbj.BJSeqOutcome.Unsure

	while outcome is None:
		action_ideal = bbj.BJStrategy.optimalFind(settings['ruleset'], cards_mine, card_dealer)
		action_player = playerGetAction(settings['ruleset'], indent, can_split)

		if action_player == bbj.BJPlayerAction.Stand:
			outcome = bbj.BJSeqOutcome.Unsure
			if action_player != action_ideal:
				strategyIsGood = False
			continue
		if action_player == bbj.BJPlayerAction.Surrender:
			outcome = bbj.BJSeqOutcome.Surrender
			if action_player != action_ideal:
				strategyIsGood = False
			continue
		if action_player == bbj.BJPlayerAction.Double:
			if len(cards_mine) > 2:
				iPrint(ColoredString("You can double only on your first two cards.\n"), sys.stderr, indent)
				continue
			if not can_split and not settings['ruleset'].allowDAS:
				iPrint(ColoredString("Table rules prohibit double after split.\n"), sys.stderr, indent)
				continue
			try:
				purse.reserve(bet)
			except PurseException as e:
				iPrint(ColoredString("Could not double: %s\n" % e), sys.stderr, indent)
				continue
			bet *= 2
			if action_player != action_ideal:
				strategyIsGood = False
		if action_player == bbj.BJPlayerAction.Double or action_player == bbj.BJPlayerAction.Hit:
			if action_player != action_ideal:
				strategyIsGood = False
			card = dealer.getCard()
			settings['cardcount'].add(card)
			dealsYou = ColoredText(ColoredString("The dealer deals you a ")) + \
				card.getStrRepr() + \
				ColoredString(".\n")
			iPrint(dealsYou, sys.stdout, indent)
			dealer.pause()
			cards_mine.append(card)
			if bbj.BJStrategy.getBestScore(cards_mine) == 21:
				outcome = bbj.BJSeqOutcome.Unsure
			elif bust(cards_mine):
				outcome = bbj.BJSeqOutcome.Bust
			elif (len(cards_mine) == 5 and settings['ruleset'].fiveCardCharlie) or action_player == bbj.BJPlayerAction.Double:
				outcome = bbj.BJSeqOutcome.Unsure
			continue
		if action_player == bbj.BJPlayerAction.Split:
			if len(cards_mine) != 2:
				iPrint(ColoredString("You can split only when you have two cards.\n"), sys.stderr, indent)
				continue
			if bbj.BJStrategy.getHardValue(cards_mine[0]) != bbj.BJStrategy.getHardValue(cards_mine[1]):
				iPrint(ColoredString("You can split only when your two cards have the same value.\n"), sys.stderr, indent)
				continue
			# Try to reserve another bet of the same amount
			try:
				purse.reserve(bet)
			except PurseException as e:
				iPrint(ColoredString("Cannot split: %s\n" % e), sys.stderr, indent)
				continue
			if action_player != action_ideal:
				strategyIsGood = False
			# now we play two independent rounds by calling this function recursively.
			indentLevel = 3	# number of spaces to indent each part of the split
			newcard = dealer.getCard()
			settings['cardcount'].add(newcard)
			iPrint(ColoredString("Let's play the first part of the split."), sys.stdout, indent)
			sys.stdout.flush()
			dealer.pause()
			dealsYouStr = ColoredText(ColoredString("  The dealer deals you a ")) + \
				newcard.getStrRepr() + \
				ColoredString(".\n")
			iPrint(dealsYouStr, sys.stdout, 0)
			outcome1 = playSequence(settings, dealer, purse, [cards_mine[0], newcard], card_dealer, bet, indent+indentLevel, False)
			newcard = dealer.getCard()
			settings['cardcount'].add(newcard)
			iPrint(ColoredString("Let's play the second part of the split."), sys.stdout, indent)
			sys.stdout.flush()
			dealer.pause()
			dealsYouStr = ColoredText(ColoredString("  The dealer deals you a ")) + \
				newcard.getStrRepr() + \
				ColoredString(".\n")
			iPrint(dealsYouStr, sys.stdout, 0)
			outcome2 = playSequence(settings, dealer, purse, [cards_mine[1], newcard], card_dealer, bet, indent+indentLevel, False)
			return [outcome1[0], outcome2[0]]
	if not strategyIsGood and settings['benevolent']:
		badStrategyColor = ColorScheme(ColorOrange, ColorOrange)
		iPrint(ColoredString("You used bad strategy.\n", badStrategyColor), sys.stdout, indent)
	if len(cards_mine) == 5 and settings['ruleset'].fiveCardCharlie and not bust(cards_mine):
		return [bbj.BJSeqOutcome.BJSeqOutcome(BJSeqOutcome.FCC, bet, payoutMultiplier, cards_mine)]
	return [bbj.BJSeqOutcome.BJSeqOutcome(outcome, bet, payoutMultiplier, cards_mine, bbj.BJStrategy.getBestScore(cards_mine))]

# playRound plays a single round, including coplayers.
# Once the round is played, playRound settles the wins and losses.
# The settlement happens in two stages: "immediate" and non-immediate wins and
# losses.  The difference is whether the dealer's hand was relevant to determine
# the winner.  For example, if the player has a Blackjack (while the dealer
# does not) or busts, the win or loss is immediate.  If the player stands at 19,
# there is neither an immediate win nor an immediate loss; the dealer plays out
# his hand and then decides who won.
# Preconditions:
# - arg 'settings': a dictionary with game settings
# - arg 'dealer': an instance of BJDealer
# - arg 'purse': an instance of Purse
# Postconditions:
# - an instance of BJRoundOutcome is returned
# - dealer and purse are affected
def playRound(settings, dealer, purse):
	bet = playerGetBet(purse, settings['ruleset'].tableMin, settings['ruleset'].tableMax)
	roundOutcome = BJRoundOutcome(bet)

	cards_dealer = [dealer.getCard(), dealer.getCard()]
	settings['cardcount'].add(cards_dealer[1])
	dealerHas = ColoredText("Dealer: ?? and ")
	dealerHas += cards_dealer[1].getStrRepr()
	dealerHas += ColoredString(".\n")
	dealerHas.display()
	dealer.pause()

	for coplayer in settings['coplayObjRight']:
		playCoplayerInitial(coplayer, settings['cardcount'], dealer)
	cards_mine = playPlayerInitial(settings['cardcount'], dealer)
	for coplayer in settings['coplayObjLeft']:
		playCoplayerInitial(coplayer, settings['cardcount'], dealer)

	# If we don't have a blackjack, the dealer's upcard is an Ace, and
	# the dealer can ask for at least a dollar for insurance, then offer insurance.
	insuranceCost = None
	if not blackjack(cards_mine) and bbj.BJStrategy.getHardValue(cards_dealer[1]) == 11:
		insuranceCost = playerGetInsuranceDecision(min(purse.getReservable(), bet/2))
		if insuranceCost is not None:
			try:
				purse.reserve(insuranceCost)
			except PurseException as e:
				# How could this happen?  I don't think it can...
				iPrint(ColoredString("Could not purchase insurance: %s.\n" % e, stream=sys.stderr), sys.stderr, indent)
				insuranceCost = None

	for coplayer in settings['coplayObjRight']:
		playCoplayer(coplayer, settings['cardcount'], dealer, cards_dealer[1])
	outcomeList = playSequence(settings, dealer, purse, cards_mine, cards_dealer[1], bet, 0, True)
	for coplayer in settings['coplayObjLeft']:
		playCoplayer(coplayer, settings['cardcount'], dealer, cards_dealer[1])

	dealerExposesForPlayer = False
	dealerExposesForCoplayer = False
	dealerPlaysForCoplayer = False
	if insuranceCost is not None:
		dealerExposesForPlayer = True
	for outcome in outcomeList:
		if outcome.outcome != bbj.BJSeqOutcome.Bust:
			dealerExposesForPlayer = True
			break
	for coplayer in settings['coplayObjLeft']+settings['coplayObjRight']:
		if coplayer.score <= 21:
			dealerExposesForCoplayer = True
			dealerPlaysForCoplayer = True

	if dealerExposesForPlayer or dealerExposesForCoplayer:
		exposesStr = ColoredText(ColoredString("The dealer exposes %s cards; %s has " % (dealer.getPronounPossessive(), dealer.getPronounSubjective()))) + \
			cards_dealer[0].getStrRepr() + \
			ColoredString(" and ") + \
			cards_dealer[1].getStrRepr() + \
			ColoredString(".\n")
		exposesStr.display()
		settings['cardcount'].add(cards_dealer[0])
		# cards_dealer[1] has already been counted
		dealer.pause()

	if dealerExposesForPlayer:
		if blackjack(cards_dealer):
			if insuranceCost is not None:
				dividend = insuranceCost * 2
				purse.release(insuranceCost)
				print("Your insurance policy pays dividends: the dealer gives you %s." % fmtMoney(dividend))
				purse.change(insuranceCost * 2)
			for outcome in outcomeList:
				# If we both don't have a Blackjack...
				if outcome.outcome != bbj.BJSeqOutcome.BJ:
					outcome.outcome = bbj.BJSeqOutcome.GenericLost
				else:
					outcome.outcome = bbj.BJSeqOutcome.Push
		else:
			if insuranceCost is not None:
				# The insurance didn't work out.
				purse.release(insuranceCost)
				print("The dealer takes your insurance money.")
				purse.change(insuranceCost * (-1))

	# Now that the dealer doesn't have a Blackjack, we reduce our bet if the player surrendered.
	for outcome in outcomeList:
		if outcome.outcome == bbj.BJSeqOutcome.Surrender:
			releasedBet = bet/2
			purse.release(releasedBet)
			outcome.bet -= releasedBet

	i = 0
	# Immediate wins, losses, or pushes, without the dealer playing out his hand
	while i < len(outcomeList):
		outcome = outcomeList[i].outcome
		if outcome < bbj.BJSeqOutcome.Unsure:
			moneyDelta = outcomeList[i].bet
			playStr = ColoredText(ColoredString("Your play ")) + \
				getPrintableListofCards(outcomeList[i].cardsPlayed) + \
				ColoredString(" loses immediately.  The dealer takes your ") + \
				ColoredString("%s.\n" % fmtMoney(moneyDelta))
			playStr.display()
			purse.release(moneyDelta)
			purse.change(moneyDelta * (-1))
			outcomeList[i:i+1] = []
		elif outcome == bbj.BJSeqOutcome.BJ or outcome == bbj.BJSeqOutcome.FCC:
			purse.release(outcomeList[i].bet)
			moneyDelta = outcomeList[i].bet * outcomeList[i].payoutMultiplier
			playStr = ColoredText(ColoredString("Your play ")) + \
				getPrintableListofCards(outcomeList[i].cardsPlayed) + \
				ColoredString(" wins immediately.  The dealer gives you ") + \
				ColoredString("%s.\n" % fmtMoney(moneyDelta))
			playStr.display()
			purse.change(moneyDelta)
			outcomeList[i:i+1] = []
		elif outcome == bbj.BJSeqOutcome.Push:
			playStr = ColoredText(ColoredString("Your play ")) + \
				getPrintableListofCards(outcomeList[i].cardsPlayed) + \
				ColoredString(" is a push.\n")
			playStr.display()
			purse.release(outcomeList[i].bet)
			outcomeList[i:i+1] = []
		else:
			i += 1
	if len(outcomeList) == 0 and not dealerPlaysForCoplayer:
		return roundOutcome

	# Dealer plays out his hand
	dealer_bestscore = bbj.BJStrategy.getBestScore(cards_dealer)
	dealer_minscore = bbj.BJStrategy.getMinScore(cards_dealer)
	while dealer_bestscore < 17 or (settings['ruleset'].hitSoft17 and dealer_bestscore == 17 and dealer_minscore < 17):
		card = dealer.getCard()
		settings['cardcount'].add(card)
		dealsSelfStr = ColoredText(ColoredString("The dealer deals %sself a " % dealer.getPronounObject())) + \
			card.getStrRepr() + \
			ColoredString(".\n")
		dealsSelfStr.display()
		dealer.pause()
		cards_dealer.append(card)
		dealer_bestscore = bbj.BJStrategy.getBestScore(cards_dealer)
		dealer_minscore = bbj.BJStrategy.getMinScore(cards_dealer)

	if len(outcomeList) == 0:
		return roundOutcome

	# The player's outcomes are not yet decided, so the dealer's hand decides.
	if bust(cards_dealer):
		for outcome in outcomeList:
			purse.release(outcome.bet)
			reward = outcome.bet * outcome.payoutMultiplier
			print("The dealer gives you %s." % fmtMoney(reward))
			purse.change(reward)
		return roundOutcome
	for outcome in outcomeList:
		purse.release(outcome.bet)
		if outcome.score > dealer_bestscore:
			moneyDelta = outcome.bet * outcome.payoutMultiplier
			playStr = ColoredText(ColoredString("Your play ")) + \
				getPrintableListofCards(outcome.cardsPlayed) + \
				ColoredString(" wins.  The dealer gives you ") + \
				ColoredString("%s.\n" % fmtMoney(moneyDelta))
			playStr.display()
			purse.change(moneyDelta)
		elif outcome.score < dealer_bestscore:
			moneyDelta = outcome.bet * (-1)
			playStr = ColoredText(ColoredString("Your play ")) + \
				getPrintableListofCards(outcome.cardsPlayed) + \
				ColoredString(" loses.  The dealer takes your ") + \
				ColoredString("%s.\n" % fmtMoney(outcome.bet))
			playStr.display()
			purse.change(moneyDelta)
		else:
			playStr = ColoredText(ColoredString("Your play ")) + \
				getPrintableListofCards(outcome.cardsPlayed) + \
				ColoredString(" is a push.\n")
			playStr.display()
	return roundOutcome

# playPlayerInitial deals cards to the main player.
# The reason this step is separate from playing these cards is that the main
# player may be in the middle of coplayers, so coplayers must be dealt their
# cards before the main player can proceed.
# Preconditions:
# - arg 'cardcountObj': an instance of BJCardCount
# - arg 'dealer': an instance of BJDealer
# Postconditions:
# - cardcountObj and dealer are affected.
def playPlayerInitial(cardcountObj, dealer):
	cards_mine = [dealer.getCard(), dealer.getCard()]
	cardcountObj.add(cards_mine[0])
	cardcountObj.add(cards_mine[1])
	receiveStr = ColoredText(ColoredString("You receive cards ")) + \
		cards_mine[0].getStrRepr() + \
		ColoredString(" and ") + \
		cards_mine[1].getStrRepr() + \
		ColoredString(".\n")
	receiveStr.display()
	dealer.pause()
	return cards_mine

# playCoplayerInitial deals cards to a coplayer.
# Preconditions:
# - arg 'coplayer': an instance of BJCoplayer
# - arg 'cardcountObj': an instance of BJCardCount
# - arg 'dealer': an instance of BJDealer
# Postconditions:
# - coplayer, cardcountObj, and dealer are affected.
def playCoplayerInitial(coplayer, cardcountObj, dealer):
	coplayer.reset()
	cardsToGive = [dealer.getCard(), dealer.getCard()]
	cardcountObj.add(cardsToGive[0])
	cardcountObj.add(cardsToGive[1])
	receivesStr = ColoredText(ColoredString("Player %s receives cards " % coplayer)) + \
		cardsToGive[0].getStrRepr() + \
		ColoredString(" and ") + \
		cardsToGive[1].getStrRepr() + \
		ColoredString(".\n")
	receivesStr.display()
	dealer.pause()
	coplayer.takeCards(cardsToGive)

# playCoplayer plays out a coplayer's hand.
# Preconditions:
# - arg 'coplayer': an instance of BJCoplayer
# - arg 'cardcountObj': an instance of BJCardCount
# - arg 'dealer': an instance of BJDealer
# - arg 'card_dealer': an instance of Card
# Postconditions:
# - coplayer, cardcountObj, and dealer are affected.
def playCoplayer(coplayer, cardcountObj, dealer, card_dealer):
	finished = False
	action = None
	while not finished:
		if coplayer.score > 21:
			finished = True
			continue
		action = coplayer.getAction(card_dealer)
		if action == bbj.BJPlayerAction.Hit:
			card = dealer.getCard()
			cardcountObj.add(card)
			hitStr = ColoredText(ColoredString("Player %s hits and gets card " % coplayer)) + \
				card.getStrRepr() + \
				ColoredString(".\n")
			hitStr.display()
			coplayer.takeCards([card])
			dealer.pause()
		elif action == bbj.BJPlayerAction.Stand:
			print("Player %s stands." % coplayer)
			finished = True
		elif action == bbj.BJPlayerAction.Double:
			card = dealer.getCard()
			cardcountObj.add(card)
			doubleStr = ColoredText(ColoredString("Player %s doubles down and gets card " % coplayer)) + \
				card.getStrRepr() + \
				ColoredString(".\n")
			doubleStr.display()
			finished = True
			dealer.pause()
		elif action == bbj.BJPlayerAction.Surrender:
			print("Player %s surrenders." % (coplayer))
			finished = True

def getPrintableListofCards(cardlist):
	if len(cardlist) == 0:
		return ColoredString("[]")
	cardStr = cardlist[0].getStrRepr() + ColoredString(",")
	for i in range(1, len(cardlist)):
		cardStr += cardlist[i].getStrRepr()
		if i < len(cardlist)-1:
			cardStr += ColoredString(",")
	cardStr = ColoredText(ColoredString("[")) + cardStr + ColoredString("]")
	return cardStr

