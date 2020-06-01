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

import datetime
import getopt
import random

from bbj.BJCardCount import BJCardCount, isStrategyKnown
from bbj.BJCardCountQuiz import BJCardCountQuiz
from bbj.BJComps import chooseComp
from bbj.BJCoplayer import BJCoplayer
from bbj.BJDealer import BJDealer, Male, Female
from bbj.BJDeck import BJDeck, numSuits
from bbj.BJGame import playRound
from bbj.Purse import Purse
from bbj.Shoe import Shoe
from bbj.Waitstaff import Waitstaff
import bbj.metadata
from bbj.money import fmtMoney
from bbj.peafowlterm import *
from bbj.BJRuleset import BJRuleset
from bbj.BJException import *

ExitNormal = 0
ExitDependUnsat = 1
ExitConfigurationProblem = 2
ExitTooPoor = 3
ExitProblem = 10

def showHeader():
	print(  "    /^^^^,  //^^^^,   ^^^^\)    Benevolent Blackjack\n" \
		"   /    /  //    /   $   //           version %s\n" \
		"  /^^^^<  //^^^^<       //\n" \
		" /    /  //    /       //  https://github.com/philipmw/benevolent-blackjack\n" \
		"/____/  //____/   \___//\n" \
		% bbj.metadata.versionstr)

def usage(progname):
	print("Syntax: %s [[argument1] [argument2] ...]" % progname)
	print("You can run Benevolent Blackjack with or without command-line arguments.")
	print("")
	print("The following arguments require a value:")
	print("\t--numdecks=4        : number of decks the shoe holds")
	print("\t--dealergender=...  : the dealer's gender: 'm' for male, 'f' for female")
	print("\t--dealerdelay=2     : number of seconds it takes the dealer to act")
	print("\t--coplayright=1     : number of coplayers to your right")
	print("\t--coplayleft=1      : number of coplayers to your left")
	print("\t--tablemin=10       : table minimum ($)")
	print("\t--tablemax=100      : table maximum ($)")
	print("\t--shufflethresh=50  : max number of cards remaining in the shoe before reshuffling")
	print("\t--bjpayout=3:2      : the Blackjack payout")
	print("\t--initbalance=500   : player's initial balance ($)")
	print("\t--countstrategy=... : card-counting strategy: ko, hi-lo, zen")
	print("\t--countquiz=0       : number of rounds between card-count quiz (0=never)")
	print("\t--coloring=darkbg   : text coloring: off, darkbg, lightbg")
	print("")
	print("The following arguments do not take a value:")
	print("\t--benevolent        : warn player when he fails to use basic strategy")
	print("\t--disallow-double   : disallow the player to double his bet")
	print("\t--disallow-surrender: disallow the player to surrender")
	print("\t--allow-das         : allow the player to double after split")
	print("\t--allow-hitsa       : allow the player to hit split Aces")
	print("\t--soft17hit         : cause the dealer to hit on Soft 17")
	print("\t--enable-5cc        : enable Five-Card Charlie")
	print("\t--show-cardcount    : show card count before every round")
	print("\nFor details, read this game's manpage and the Blackjack page on Wikipedia.")

# getGameSettings processes the command-line arguments.
# Preconditions: none
# Postconditions:
# - returns:
#   - a dictionary with settings if everything is fine;
#   - None if no noteworthy error occurred yet we cannot start a game;
# - an exception is raised if a noteworthy error occurs
def getGameSettings(args):
	settings = {}
	settings['ruleset'] = BJRuleset(
		4,			# number of decks
		10,			# table minimum
		100,		# table maximum
		50,			# reshuffle when <= cards remain
		{'n':3, 'd':2},	# Blackjack payout
		True,		# allow double
		True,		# allow surrender
		False,		# allow double after split
		False,		# allow hit on split aces
		False,		# hit soft 17
		False,		# five card charlie
	)
	settings['dealergender'] = Male if random.randint(0, 1) == 1 else Female
	settings['coplayright'] = 1
	settings['coplayleft'] = 1
	settings['dealerdelay'] = 2
	settings['initbalance'] = 500
	settings['benevolent'] = False
	settings['cardcount'] = BJCardCount()
	settings['cardcount-quiz'] = 0
	settings['cardcount-show'] = False
	try:
		opts, args = getopt.getopt(args, '', [
			'help',
			'version',
			'dealergender=',
			'numdecks=',
			'coplayright=',
			'coplayleft=',
			'dealerdelay=',
			'tablemin=',
			'tablemax=',
			'shufflethresh=',
			'bjpayout=',
			'initbalance=',
			'countstrategy=',
			'countquiz=',
			'coloring=',
			'benevolent',
			'disallow-double',
			'disallow-surrender',
			'allow-das',
			'allow-hitsa',
			'soft17hit',
			'enable-5cc',
			'show-cardcount',
		])
	except getopt.GetoptError as e:
		print(e)
		return None

	for o, a in opts:
		if o == '--help':
			usage(sys.argv[0])
			return None
		if o == '--version':
			print("%s" % bbj.metadata.versionstr)
			return None
		elif o == '--dealergender':
			if a == 'm' or a == 'f':
				settings['dealergender'] = Male if a == 'm' else Female
			else:
				raise BJException("The dealer gender must be 'm' for male or 'f' for female.")
		elif o == '--numdecks':
			try:
				v = int(a)
			except ValueError:
				raise BJException("The number of decks must be an integer.")
			settings['ruleset'].numDecksSet(v)
		elif o == '--coplayleft' or o == '--coplayright':
			try:
				v = int(a)
			except ValueError:
				raise BJException("The number of coplayers must be an integer.")
			if v < 0:
				raise BJException("The number of coplayers must be non-negative.")
			if o == '--coplayleft':
				settings['coplayleft'] = v
			else:
				settings['coplayright'] = v
		elif o == '--dealerdelay':
			try:
				v = int(a)
			except ValueError:
				raise BJException("The dealer delay must be an integer.")
			if v < 0:
				raise BJException("The dealer delay must be non-negative.")
			settings['dealerdelay'] = v
		elif o == '--tablemin':
			try:
				v = int(a)
			except ValueError:
				raise BJException("The table minimum must be an integer.")
			settings['ruleset'].tableMinSet(v)
		elif o == '--tablemax':
			try:
				v = int(a)
			except ValueError:
				raise BJException("The table maximum must be an integer.")
			settings['ruleset'].tableMaxSet(v)
		elif o == '--shufflethresh':
			try:
				v = int(a)
			except ValueError:
				raise BJException("The shuffle threshold must be an integer.")
			settings['ruleset'].reshuffleThresholdSet(v)
		elif o == '--bjpayout':
			colon = a.find(':')
			if colon is None:
				raise BJException("The Blackjack payout is malformed; must be '#:#'.")
			try:
				numer = int(a[:colon])
				denom = int(a[colon+1:])
			except ValueError:
				raise BJException("The Blackjack payout is malformed; must be '#:#'.")
			settings['ruleset'].blackjackPayoutSet({'n': numer, 'd': denom})
		elif o == '--initbalance':
			try:
				v = int(a)
			except ValueError:
				raise BJException("The initial balance must be an integer.")
			if v <= 0:
				raise BJException("The initial balance must be positive.")
			settings['initbalance'] = v
		elif o == '--countstrategy':
			if not isStrategyKnown(a):
				raise BJException("The name of the card-counting strategy is unrecognized.")
			settings['cardcount'] = BJCardCount(a)
		elif o == '--countquiz':
			try:
				v = int(a)
			except ValueError:
				raise BJException("The card-count quiz interval must be an integer.")
			if v < 0:
				raise BJException("The card-count quiz interval must be non-negative.")
			settings['cardcount-quiz'] = v
			settings['cardcount-quizObj'] = BJCardCountQuiz()
		elif o == '--coloring':
			if not coloringSupported():
				raise BJException("Terminal colors are not supported in your environment.")
			try:
				coloringSet(a)
			except PeafowltermError as e:
				raise BJException("Coloring setting rejected: %s" % e)
		elif o == '--benevolent':
			settings['benevolent'] = True
		elif o == '--disallow-double':
			settings['ruleset'].allowDoubleSet(False)
		elif o == '--disallow-surrender':
			settings['ruleset'].allowSurrenderSet(False)
		elif o == '--allow-das':
			settings['ruleset'].allowDASSet(True)
		elif o == '--allow-hitsa':
			settings['ruleset'].allowHitSplitAcesSet(True)
		elif o == '--soft17hit':
			settings['ruleset'].hitSoft17Set(True)
		elif o == '--enable-5cc':
			settings['ruleset'].fiveCardCharlieSet(True)
		elif o == '--show-cardcount':
			settings['cardcount-show'] = True

	# Check for consistency
	if settings['ruleset'].tableMin > settings['ruleset'].tableMax:
		raise BJException("The table minimum must not be greater than the table maximum.")
	if settings['cardcount-show'] and not settings['cardcount'].isEnabled():
		raise BJException("To show card count, a card-counting strategy must be selected.")
	if settings['cardcount-quiz'] and not settings['cardcount'].isEnabled():
		raise BJException("To quiz about the card count, a card-counting strategy must be selected.")
	if settings['coplayleft'] + settings['coplayright'] > 6:
		raise BJException("The maximum number of players, including yourself, at a table is 7.")

	return settings

# findMaxCardsRequired finds the maximum number of cards that can be used
# during one round.
# Preconditions:
# - arg 'numDecks' is an integer
# - arg 'numPlayersAtTable' is an integer
# - BJDeck has an integer 'numSuits'
# Postconditions:
# - an integer is returned
def findMaxCardsRequired(numDecks, numPlayersAtTable):
	def findMaxCardsForSequence(requiredScore, lowestValueAvail, cardValueNum):
		valueAccumulator = 0
		cardsUsed = 0
		while valueAccumulator < requiredScore:
			cardsUsed += 1
			valueAccumulator += lowestValueAvail
			cardValueNum += 1
			if cardValueNum >= numCardsPerValue:
				lowestValueAvail += 1
				cardValueNum = 0
		return lowestValueAvail, cardValueNum, cardsUsed

	numCardsPerValue = numDecks * numSuits
	# The required score is 18 points for the dealer since he may have to hit on soft 17
	lowestValueAvail, cardValueNum, cardsUsed = findMaxCardsForSequence(18, 1, 0)
	# Here we have one more iteration than the number of players because
	# the main player can split.
	for i in range(numPlayersAtTable+1):
		# The required score is 21 points for a player.
		lowestValueAvail, cardValueNum, tmp = findMaxCardsForSequence(21, lowestValueAvail, cardValueNum)
		cardsUsed += tmp
	return cardsUsed

# playerQuizCardCount asks the user for his estimate of the current cardcount
# and returns this response.
# Preconditions: none
# Postconditions:
# - an integer is returned
def playerQuizCardCount():
	gotit = False
	while not gotit:
		quizColor = ColorScheme(ColorRed, ColorRed)
		quizStr = ColoredString("QUIZ: What is the current card count? ", quizColor)
		quizStr.display()
		try:
			answer = int(sys.stdin.readline().strip())
			gotit = True
		except (TypeError, ValueError):
			sys.stderr.write("You must enter an integer.\n")
	return answer

# cardcountStatsShow shows the player how accurate his card-counting was
# since the last time that statistics were cleared.
# Preconditions:
# - quizObj is an instance of BJCardCountQuiz
# Postconditions: none
def cardcountStatsShow(quizObj):
	# the first element of 'ranges' should be (-sys.maxint).
	ranges = [-sys.maxint, -4, -3, -2, -1, 0, 1, 2, 3, 4]
	numGuesses = quizObj.guessGetQuantity()
	if numGuesses < 1:
		return
	print("== Card-Counting Quiz Statistics ==")
	guessSuccessList = quizObj.guessGetGroup(ranges)
	for i in range(len(guessSuccessList)):
		if guessSuccessList[i] == 0:
			continue
		if ranges[i] == 0:
			descr = "correct"
		else:
			if i < len(ranges)-1 and ranges[i]+1 == ranges[i+1]:
				descr = "off by %+d" % ranges[i]
			else:
				descr = "off by %s, %s" % (
					u"( -\u221e" if i == 0 else ("[%+3d" % ranges[i]),
					u"  \u221e)" if i == len(ranges)-1 else ("%+3d)" % ranges[i+1])
				)
		print("You were %-17s: %3d out of %3d times (%5.1f%%)." % (
			descr,
			guessSuccessList[i],
			numGuesses,
			100.0*guessSuccessList[i]/numGuesses,
		))

# timeDiffGetminutes returns the number of minutes represented by a timedelta
# object.
# Preconditions:
# - timediff is an instance of datetime.timedelta
# Postconditions:
# - an integer is returned
def timeDiffGetMinutes(timediff):
	mins = timediff.days * 24 * 60
	mins += int(round(timediff.seconds / 60.0))
	return mins

# timeDiffGetStr returns a user-friendly string representation of a timedelta
# object.
# Preconditions:
# - timediff is an instance of datetime.timedelta
# Postconditions:
# - a string is returned
def timeDiffGetStr(timediff):
	s = ""
	if timediff.days > 0:
		s += "%d day%s" % (timediff.days, "" if timediff.days == 1 else "s")
		if hours > 0 or minutes > 0:
			s += ", "
	hours = timediff.seconds / (60*60)
	minutes = int(round((timediff.seconds - (60*60*hours)) / 60.0))
	if hours > 0:
		s += "%d hour%s" % (hours, "" if hours == 1 else "s")
		if minutes > 0:
			s += " and "
	if minutes > 0:
		s += "%d minute%s" % (minutes, "" if minutes == 1 else "s")
	if s == "":
		s = "less than a minute"
	return s

# reshuffle refills the shoe with fresh cards.
# Preconditions:
# - arg 'dealer' is an instance of BJDealer
# - arg 'settings' is a dictionary of game settings
# Postconditions:
# - dealer's shoe is affected
# - cardcount quiz (living inside settings) is affected
def reshuffle(dealer, settings):
	reshuffleStr = ColoredString("It's time to reshuffle the shoe of cards.\n", ColorScheme(ColorTeal, ColorTeal))
	reshuffleStr.display()
	if settings['cardcount-quiz'] > 0:
		intervalOffsets = settings['cardcount-quizObj'].intervalGetOffsets()
		settings['cardcount-quizObj'].intervalClear()
		if len(intervalOffsets) > 0:
			print("During this interval of gameplay, here's how your card-counting fared:")
			quiznum = 0
			for offset in intervalOffsets:
				quiznum += 1
				print(" - on quiz #%d, you were %s." % (
					quiznum,
					("correct" if offset == 0 else ("off by %+d from true count" % offset))
				))
	sys.stdout.write("Shuffling")
	for i in range(7):
		sys.stdout.write('.')
		sys.stdout.flush()
		dealer.pause()
	dealer.reshuffleShoe()
	settings['cardcount'].reset()
	sys.stdout.write('\n')
	print("The shoe is reshuffled.")

# This is the entrypoint.
# Preconditions: none
# Postconditions:
# - an integer is returned suitable for returning to the operating system
def run():
	try:
		settings = getGameSettings(sys.argv[1:])
	except BJException as e:
		sys.stderr.write("Error: %s\n" % e)
		return ExitConfigurationProblem
	if settings is None:
		return ExitNormal
	showHeader()

	dealer = BJDealer(settings['dealergender'], Shoe(settings['ruleset'].numDecks, BJDeck), settings['ruleset'].reshuffleThreshold, settings['dealerdelay'])
	del settings['dealergender']
	del settings['dealerdelay']
	purse = Purse(settings['initbalance'], False)
	# Initialize coplayers
	settings['coplayObjRight'] = []
	settings['coplayObjLeft'] = []
	for i in range(settings['coplayright']):
		settings['coplayObjRight'].append(BJCoplayer())
	for i in range(settings['coplayleft']):
		settings['coplayObjLeft'].append(BJCoplayer())
	
	print(settings['ruleset'])
	print("== Game Settings ==")
	print("\tBenevolent:              %s" % ("yes" if settings['benevolent'] else "no"))
	print("\tCoplayers to your right: %d" % settings['coplayleft'])
	print("\tCoplayers to your left:  %d" % settings['coplayleft'])
	print("\tDealer gender:           %s" % ('male' if dealer.gender == Male else 'female'))
	print("\tDealer delay:            %d seconds" % dealer.delay)
	print("\tCard counting strategy:  %s" % settings['cardcount'])
	print("\tShow card count:         %s" % ("yes" if settings['cardcount-show'] else "no"))
	print("\tQuiz card count:         %s" % (("every %d hands" % settings['cardcount-quiz']) if settings['cardcount-quiz'] > 0 else "not enabled"))
	print("\tColoring:                %s" % coloringGetStr())
	print("")
	print("To change settings, rerun BBJ with a '--help' argument.")
	print("To walk away from the table, press Ctrl-C at any time.")

	# See if the reshuffle is sufficiently frequent.
	numPlayersAtTable = settings['coplayleft']+settings['coplayright']+1
	minShoeSize = findMaxCardsRequired(settings['ruleset'].numDecks, numPlayersAtTable)
	# With minShoeSize we can safely start a new round; we do not need to reshuffle yet.
	# Reshuffling needs to happen at minShoeSize-1 or below.
	if settings['ruleset'].reshuffleThreshold < minShoeSize-1:
		sys.stderr.write("\n-- Warning: --\n")
		sys.stderr.write("Your reshuffle threshold is too low; it's possible to run out of cards during a single round.\n")
		sys.stderr.write("With %d players at the table, %d deck(s) should be reshuffled when shoe has %d cards or fewer.\n" % (numPlayersAtTable, settings['ruleset'].numDecks, minShoeSize-1))
		sys.stderr.write("\n")

	waitstaff = Waitstaff(settings['ruleset'].tableMin)
	retcode = None
	rounds_played = 0
	total_wagered = 0
	ts_start = datetime.datetime.now()
	while retcode is None:
		waitstaff.makeRound()
		print("")
		try:
			if settings['cardcount-quiz'] > 0 and rounds_played > 0 and rounds_played % settings['cardcount-quiz'] == 0:
				guess = playerQuizCardCount()
				settings['cardcount-quizObj'].guessMake(guess, settings['cardcount'].get())
			if settings['cardcount'].isEnabled() and settings['cardcount-show']:
				print("Current card count: %d" % settings['cardcount'].get())
			roundOutcome = playRound(settings, dealer, purse)
			total_wagered += roundOutcome.bet
			rounds_played += 1
		except BJException as e:
			sys.stderr.write("Error: %s\n" % e)
			retcode = ExitProblem
			continue
		except KeyboardInterrupt:
			retcode = ExitNormal
			continue
	
		print("")
		if purse.getBalance() < settings['ruleset'].tableMin:
			print("Your balance falls below the table minimum.\nThe casino shoves you out into the street.")
			retcode = ExitTooPoor
			continue
		if dealer.shouldReshuffle():
			try:
				reshuffle(dealer, settings)
			except KeyboardInterrupt:
				retcode = ExitNormal
				continue
			min_threshold = 2
			if settings['coplayleft']+settings['coplayright'] >= min_threshold and random.randint(0, (settings['coplayleft']+settings['coplayright'])-min_threshold+1) != 0:
				print("Some players at your table cashed out and left.  Others take their seats.")
			print("")
	ts_finish = datetime.datetime.now()
	print("")

	money_diff = purse.getBalance() - settings['initbalance']
	time_diff = ts_finish - ts_start
	print("You played %d rounds and %s %s in %s." % (
		rounds_played,
		'won' if money_diff >= 0 else 'lost',
		fmtMoney(abs(money_diff)),
		timeDiffGetStr(time_diff),
		))
	mins_played = timeDiffGetMinutes(time_diff)
	if rounds_played > 0 and mins_played > 0:
		print("That's about %d rounds/hour, %s/round, and %s/hour." % (
			(rounds_played * 60 / mins_played),
			fmtMoney(money_diff / rounds_played),
			fmtMoney(money_diff * 60 / mins_played),
		))

	if settings['cardcount-quiz'] > 0:
		print("")
		cardcountStatsShow(settings['cardcount-quizObj'])

	comp = chooseComp(rounds_played, mins_played, total_wagered)
	if comp is not None:
		print("")
		print("Before you leave, the pit boss pulls you aside and thanks you for your patronage.")
		print("You receive %s!" % comp)

	return retcode
