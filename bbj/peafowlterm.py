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

import copy
import ctypes
from io import IOBase
import sys

class LLNode:
	def __init__(self, v):
		self.v = v
		self.next = None

	def append(self, v):
		if isinstance(v, LLNode):
			self.__getLastNode().next = v
		else:
			self.__getLastNode().next = LLNode(v)

	def __str__(self):
		return str(self.v)

	def __iter__(self):
		n = self
		while n is not None:
			yield n
			n = n.next

	def __getLastNode(self):
		n = self
		while n.next is not None:
			n = n.next
		return n

class LinkedList:
	def __init__(self, v):
		self.head = LLNode(v)

	def prepend(self, v):
		newnode = LLNode(v)
		newnode.next = self.head
		self.head = newnode

	def append(self, v):
		self.head.append(v)

	def __iter__(self):
		for n in self.head:
			yield n.v

	def __copy__(self):
		newhead = None
		currnode = None
		for node in self:
			newnode = LLNode(node.v)
			if newhead is None:
				newhead = newnode
			else:
				currnode.append(newnode)
			currnode = newnode
		return newhead

	def __str__(self):
		s = "["
		for n in self.head:
			s += "%s, " % n.v
		s = s[:-2] # remove comma and space
		s += "]"
		return s

class PeafowltermError(BaseException):
	pass

class Color:
	"""
	This class defines a known color.  The attributes of a color are its
	name (such as "yellow"), its Unix color code, such as 33 for yellow,
	and whether it's bold.
	"""
	def __init__(self, name, unixColorCode, bold):
		if not isinstance(name, str):
			raise PeafowltermError('Given color name must be a string.')
		self.__name = name
		if not isinstance(unixColorCode, int) and unixColorCode is not None:
			raise PeafowltermError('Given Unix color code must be an integer or None.')
		self.__unixColorCode = unixColorCode
		if not isinstance(bold, bool):
			raise PeafowltermError('Given boldness must be boolean.')
		self.__bold = bold

	def getName(self):
		"""
		Returns the name of the color as a string.
		"""
		return self.__name

	def hasColor(self):
		"""
		Returns True if this Color instance has a color code.
		This is false only when this Color instance affects only boldness.
		"""
		if self.__unixColorCode is not None:
			return True
		return False

	def getUCC(self):
		"""
		Returns the integer that is the Unix color code (escape sequence)
		for this color.
		"""
		return self.__unixColorCode

	def isBold(self):
		"""
		Returns True if this Color instance enables boldness, and False
		otherwise.
		"""
		return self.__bold

class ColorScheme:
	"""
	This class defines a color scheme which is then attached to one or more
	strings.  The color scheme indicates the string's colors for both light
	and dark backgrounds.
	"""
	def __init__(self, darkColorFg=None, lightColorFg=None):
		self.setDarkColorFg(darkColorFg)
		self.setLightColorFg(lightColorFg)

	def setDarkColorFg(self, color):
		"""
		Sets the foreground color for a dark background.
		Returns self.
		"""
		if not isinstance(color, Color) and color is not None:
			raise PeafowltermError('Given color must be a Color object or None.')
		self.__darkColorFg = color
		return self

	def setLightColorFg(self, color):
		"""
		Sets the foreground color for a light background.
		Returns self.
		"""
		if not isinstance(color, Color) and color is not None:
			raise PeafowltermError('Given color must be a Color object or None.')
		self.__lightColorFg = color
		return self

	def getDarkColorFg(self):
		"""
		Returns the current foreground color for a dark background.
		"""
		return self.__darkColorFg

	def getLightColorFg(self):
		"""
		Returns the current foreground color for a light background.
		"""
		return self.__lightColorFg

class ColoredString:
	"""
	This class bundles a text string with a color scheme and a destination
	stream.  The class offers a display() method that writes the colored
	string to the stream.
	"""
	def __init__(self, msg, colorScheme=None, stream=sys.stdout):
		import codecs
		if not isinstance(msg, str):
			raise PeafowltermError("Given message must be a string instance.")
		if colorScheme is not None and not isinstance(colorScheme, ColorScheme):
			raise PeafowltermError("Given color scheme must be a ColorScheme instance.")
		if not isinstance(stream, IOBase) and not isinstance(stream, codecs.StreamWriter):
			raise PeafowltermError("Given stream must be a file or codecs.StreamWriter instance.")
		self.msg = msg
		self.colorScheme = colorScheme
		self.stream = stream

	def __add__(self, v):
		"""
		Simply calls append() with the given value.
		"""
		return self.append(v)

	def append(self, v):
		"""
		Appends a string to the existing string inside of this instance.
		Returns self.
		"""
		if v is None:
			return self
		if isinstance(v, str):
			self.msg += v
			return self
		raise PeafowltermError("To ColoredString you can add only strings.")

	def display(self):
		"""
		Writes the colored string to the stream associated with this instance.
		Does not return anything.
		"""
		import os

		if coloring == ColorSettingOff or self.colorScheme is None:
			self.stream.write(self.msg)
			return
		if coloring == ColorSettingBGDark:
			color = self.colorScheme.getDarkColorFg()
		else:
			color = self.colorScheme.getLightColorFg()
		if os.name == 'nt':
			self.__displayNT(color)
		else:
			self.__displayUnix(color)

	def __displayNT(self, color):
		def getBufferInfo(handle):
			import struct
			bufinfo = ctypes.create_string_buffer(22) # CONSOLE_SCREEN_BUFFER_INFO structure
			res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, bufinfo)
			assert res

			(bufx, bufy, curx, cury,
			 wattr,
			 left, top, right, bottom,
			 maxx, maxy) = struct.unpack("hhhhHhhhhhh", bufinfo.raw)
			return wattr

		(winhandle, wincolor) = self.__settingsTranslateUnixToWin(self.stream, color)
		prevcolor = getBufferInfo(winhandle)
		ctypes.windll.kernel32.SetConsoleTextAttribute(winhandle, wincolor)
		self.stream.write(self.msg)
		ctypes.windll.kernel32.SetConsoleTextAttribute(winhandle, prevcolor) # reset color

	def __displayUnix(self, color):
		if color is None:
			# just the message, ma'am
			output = self.msg
		else:
			output = '\033['
			if color.hasColor():
				output += '%d' % color.getUCC()
			if color.isBold():
				if color.hasColor():
					output += ';'
				output += '1'
			output += 'm'
			output += self.msg
			output += '\033[0m'
		self.stream.write(output)

	# settingsTranslateUnixToWin changes Unix-specific settings to their
	# Windows-specific counterparts.
	# Preconditions: stream and Color object must be valid for Unix.
	# Postconditions: a winhandle and a Windows-specific color settings are returned.
	@staticmethod
	def __settingsTranslateUnixToWin(stream, color):
		STD_INPUT_HANDLE = -10
		STD_OUTPUT_HANDLE= -11
		STD_ERROR_HANDLE = -12
		FOREGROUND_BLUE = 0x01 # text color contains blue.
		FOREGROUND_GREEN= 0x02 # text color contains green.
		FOREGROUND_RED  = 0x04 # text color contains red.
		FOREGROUND_INTENSITY = 0x08 # text color is intensified.
		BACKGROUND_BLUE = 0x10 # background color contains blue.
		BACKGROUND_GREEN= 0x20 # background color contains green.
		BACKGROUND_RED  = 0x40 # background color contains red.
		BACKGROUND_INTENSITY = 0x80 # background color is intensified.
		# translate to Windows-specific constants
		if stream == sys.stdout or (hasattr(stream, 'stream') and stream.stream == sys.stdout):
			winhandle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
		elif stream == sys.stderr or (hasattr(stream, 'stream') and stream.stream == sys.stderr):
			winhandle = ctypes.windll.kernel32.GetStdHandle(STD_ERROR_HANDLE)
		else:
			raise PeafowltermError("unknown stream requested")
		if color == ColorBrown:
			color = FOREGROUND_RED
		elif color == ColorRed:
			color = FOREGROUND_RED | FOREGROUND_INTENSITY
		elif color == ColorGreen:
			color = FOREGROUND_GREEN
		elif color == ColorLime:
			color = FOREGROUND_GREEN | FOREGROUND_INTENSITY
		elif color == ColorOrange:
			color = FOREGROUND_RED | FOREGROUND_GREEN
		elif color == ColorYellow:
			color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY
		elif color == ColorNavy:
			color = FOREGROUND_BLUE
		elif color == ColorBlue:
			color = FOREGROUND_BLUE | FOREGROUND_INTENSITY
		elif color == ColorPurple:
			color = FOREGROUND_RED | FOREGROUND_BLUE
		elif color == ColorPink:
			color = FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY
		elif color == ColorTeal:
			color = FOREGROUND_GREEN | FOREGROUND_BLUE
		elif color == ColorAqua:
			color = FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY
		elif color == ColorGray:
			color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE
		elif color == ColorGray:
			color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY
		else:
			color = 0x0
		return (winhandle, color)

class ColoredText(LinkedList):
	"""
	This class allows the programmer to combine ColoredStrings, such that
	one object represents (possibly) multiple strings in different colors.
	ColoredStrings are combined by ColoredText in a linked list data
	structure.
	"""

	def __init__(self, v):
		if isinstance(v, str):
			v = ColoredString(v)
		if not isinstance(v, ColoredString):
			raise PeafowltermError('ColoredText must be initialized with a ColoredString or a string.')
		LinkedList.__init__(self, v)

	def display(self):
		"""
		Displays all strings that comprise this text.
		The strings are written to their respective streams with their
		respective colors.
		Does not return anything.
		"""
		for n in self:
			n.display()

	def append(self, newnode):
		"""
		Appends a (possibly colored) string to the existing set of
		strings that comprise this text.  The input can be a regular
		string, an instance of ColoredString, or an instance of
		ColoredText.  If the input is ColoredText, its strings ("nodes")
		are not duplicated; instead, new references to these nodes are
		attached to the current ColoredText.
		Returns self.
		"""
		if newnode is None:
			return self
		if isinstance(newnode, str):
			newnode = ColoredString(newnode)
		if not isinstance(newnode, ColoredString) and not isinstance(newnode, ColoredText):
			raise PeafowltermError("To ColoredText you can append only strings or instances of ColoredString or ColoredText.")
		LinkedList.append(self, newnode)
		return self

	def __add__(self, newnode):
		"""
		Simply calls append() with the given value.
		"""
		return self.append(newnode)

	def __copy__(self):
		thecopy = None
		for node in self:
			nodecopy = copy.copy(node)
			if thecopy is None:
				thecopy = ColoredText(nodecopy)
			else:
				thecopy.append(nodecopy)
		return thecopy

ColorBrown = Color("brown", 31, False)
ColorRed = Color("red", 31, True)
ColorGreen = Color("green", 32, False)
ColorLime = Color("lime", 32, True)
ColorOrange = Color("orange", 33, False)
ColorYellow = Color("yellow", 33, True)
ColorNavy = Color("navy", 34, False)
ColorBlue = Color("blue", 34, True)
ColorPurple = Color("purple", 35, False)
ColorPink = Color("pink", 35, True)
ColorTeal = Color("teal", 36, False)
ColorAqua = Color("aqua", 36, True)
ColorGray = Color("gray", 37, False)
ColorWhite = Color("white", 37, True)
ColorBold = Color("bold", None, True)

ColorPalette = [ColorBrown, ColorRed, ColorGreen, ColorLime,
		ColorOrange, ColorYellow, ColorNavy, ColorBlue,
		ColorPurple, ColorPink, ColorTeal, ColorAqua,
		ColorGray, ColorWhite, ColorBold]

ColorSettingOff = 0
ColorSettingBGDark = 1
ColorSettingBGLight = 2

coloring = ColorSettingBGDark

# Preconditions: none
# Postconditions:
# - returns True if coloring is supported; else False
def coloringSupported():
	"""
	Returns True if coloring is supported in the current environment,
	and False otherwise.
	"""
	# FIXME: how do we figure out if coloring is unsupported?
	return True

# Preconditions:
# - arg 'setting': one of the ColorSetting... values
# Postconditions:
# - affects the change or raises a PeafowltermError.
def coloringSet(setting):
	"""
	Memorizes a user's desired coloring scheme using a global variable.
	Does not return anything.
	"""
	global coloring

	if not coloringSupported():
		raise PeafowltermError("coloring is not supported")

	if setting == "off":
		coloring = ColorSettingOff
	elif setting == "darkbg":
		coloring = ColorSettingBGDark
	elif setting == "lightbg":
		coloring = ColorSettingBGLight
	else:
		raise PeafowltermError("given color setting is unrecognized")

# coloringGetStr returns a textual representation of the current coloring
# scheme.
# Preconditions: none
# Postconditions:
# - a string is returned
def coloringGetStr():
	if coloring == ColorSettingOff:
		return "off"
	elif coloring == ColorSettingBGDark:
		return "colored for dark background"
	elif coloring == ColorSettingBGLight:
		return "colored for light background"
	else:
		return "[unrecognized]"
