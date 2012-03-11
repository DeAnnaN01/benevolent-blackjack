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

Hit = 0
Stand = 1
Double = 2
Split = 3
Surrender = 4

# Preconditions:
# - arg 'v': one of the actions defined in this file
# Postconditions:
# - a string representation of the action is returned
def str(v):
	if v == Hit:
		return "hit"
	if v == Stand:
		return "stand"
	if v == Double:
		return "double"
	if v == Split:
		return "split"
	if v == Surrender:
		return "surrender"
