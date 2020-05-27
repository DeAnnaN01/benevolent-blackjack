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

def fmtMoney(amt):
    # I am intentionally not using locale here because it is too much of a PITA.
    return "${:,.0f}".format(amt)
