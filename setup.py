#!/bin/env python

from distutils.core import setup
import bbj.metadata

setup(name = "Benevolent Blackjack",
	version = bbj.metadata.versionstr,
	description = bbj.metadata.description,
	author = bbj.metadata.author,
	author_email = bbj.metadata.author_email,
	url = bbj.metadata.homepage,
	packages = ['bbj'],
	scripts = ['bin/bbj'],
	license = bbj.metadata.copyright + \
		", licensed under the GNU General Public License version 3"
)
