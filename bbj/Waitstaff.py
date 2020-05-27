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

class Waitstaff:
	def __init__(self, tableMin):
		self.tableMin = tableMin
		if tableMin < 5:
			# we don't serve your kind here
			self.period = None
		else:
			self.period = int(60.0/int(tableMin) + 11)

	def makeRound(self):
		if self.period is None:
			return
		if random.randint(0, self.period) == 0:
			print("A waitress comes around the table and gives you a drink.")
