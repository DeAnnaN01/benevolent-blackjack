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

# Instances of Money are monetary values.  They support comparisons and
# arithmetic operations.
class Money:
	def __init__(self, *args):
		if len(args) == 1:
			moneyObj = args[0]
			if not isinstance(moneyObj, Money):
				raise TypeError, "Either instantiate Money with Money, or provide a prefix and suffix."
			self.__init__(moneyObj.prefix, moneyObj.amountmoney, Obj.suffix)
		elif len(args) == 3:
			prefix, amount, suffix = args
			self.prefix = prefix
			self.amount = amount
			self.suffix = suffix
			self.textize()
		else:
			raise Exception, "Money is incorrectly instantiated"

	def __int__(self):
		return self.amount

	def __float__(self):
		return float(self.amount)

	def __cmp__(self, o):
		if isinstance(o, int):
			return self.value() - o
		elif isinstance(o, Money):
			return self.value() - o.value()
		else:
			raise TypeError, "Only integers and Money objects can be compared to Money objects."

	def __add__(self, o):
		if isinstance(o, int):
			return Money(self.prefix, self.value() + o, self.suffix)
		elif isinstance(o, Money):
			return Money(self.prefix, self.value() + o.value(), self.suffix)
		else:
			raise TypeError, "Only integers and Money objects can be added to Money objects."

	def __sub__(self, o):
		if isinstance(o, int):
			return Money(self.prefix, self.value() - o, self.suffix)
		elif isinstance(o, Money):
			return Money(self.prefix, self.value() - o.value(), self.suffix)
		else:
			raise TypeError, "Only integers and Money objects can be added to Money objects."

	def __mul__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			return Money(self.prefix, int(self.value() * o), self.suffix)
		else:
			raise TypeError, "Only integers and floats can multiply Money objects."

	def __div__(self, o):
		if isinstance(o, int):
			return Money(self.prefix, self.value() / o, self.suffix)
		else:
			raise TypeError, "Only integers can divide Money objects."

	def __abs__(self):
		if self.value() < 0:
			return self * (-1)
		return self

	def textize(self):
		text = ""
		amount = self.amount
		isNegative = False
		if amount < 0:
			isNegative = True
			amount *= -1
		digitNum = 0
		while amount > 0:
			text = str(amount % 10) + text
			amount /= 10
			digitNum += 1
			if digitNum % 3 == 0 and amount > 0:
				text = "," + text
		if digitNum == 0:
			text = "0"
		elif isNegative:
			text = "-" + text
		self.text = self.prefix + text + self.suffix

	def value(self):
		return self.amount

	def __str__(self):
		return self.text
