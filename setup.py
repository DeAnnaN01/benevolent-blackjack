#!/usr/bin/env python3

from setuptools import setup, find_packages

import bbj.metadata

setup(name = "Benevolent Blackjack",
	version = bbj.metadata.versionstr,
	description = bbj.metadata.description,
  long_description = """
Benevolent Blackjack is a cross-platform console-based program that plays a [game of Blackjack](https://en.wikipedia.org/wiki/Blackjack) with you, acting as the dealer and (optionally) any number of co-players.
In addition to being able to play the role of an apathetic dealer, Benevolent Blackjack has two unique features: it can benevolently advise you on whether you are [making optimal decisions](https://en.wikipedia.org/wiki/Blackjack#Basic_strategy) to minimize the house edge, and it can train you to count cards.
""",
  long_description_content_type="text/markdown",
	author = bbj.metadata.author,
	author_email = bbj.metadata.author_email,
	url = bbj.metadata.homepage,
	packages = ['bbj'],
	license = bbj.metadata.copyright + \
		", licensed under the GNU General Public License version 3",
  classifiers = [
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Topic :: Games/Entertainment",
  ]
)
