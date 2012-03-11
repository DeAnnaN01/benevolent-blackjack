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

from Money import *

# A subclass of Money, Dollars adds a dollar symbol in front.
class Dollars(Money):
	def __init__(self, value):
		if isinstance(value, Money):
			Money.__init__(self, value)
		elif isinstance(value, int):
			Money.__init__(self, "$", value, "")
		else:
			raise TypeError, "Dollars must be instantiated either with Money or an integer."
