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

from bbj.money import fmtMoney

class PurseException(BaseException):
	pass

# An instance of Purse holds money.  Additionally, some amount of money in the
# purse can be reserved, which means the balance is unchanged but the reserved
# amount cannot be spent until it has been released.  This feature is similar
# to the "holds" that US banks occasionally place on one's balance.
class Purse:
	def __init__(self, amt, verbose=False):
		self.balance = amt
		self.verbose = verbose
		self.reserved = 0

	def canReserve(self, amt):
		if amt < 0:
			return False
		if self.balance < self.reserved + amt:
			return False
		return True

	def reserve(self, amt):
		if amt < 0:
			raise PurseException("Cannot reserve a negative amount.")
		if self.balance < self.reserved + amt:
			raise PurseException("Insufficient balance.")
		self.reserved += amt

	def release(self, amt):
		if amt < 0:
			raise PurseException("Cannot release a negative amount.")
		if amt > self.reserved:
			raise PurseException("Cannot release more than is reserved.")
		self.reserved -= amt

	def change(self, amount):
		if amount == 0:
			return
		self.balance += amount
		if amount > 0:
			self.selectivePrint("Your balance increases by %s." % fmtMoney(amount))
		else:
			self.selectivePrint("Your balance decreases by %s." % fmtMoney(amount*(-1)))

	def getReservable(self):
		return self.balance - self.reserved

	def getBalance(self):
		return self.balance

	def selectivePrint(self, msg):
		if self.verbose:
			print(msg)

	def __str__(self):
		return fmtMoney(self.balance)
