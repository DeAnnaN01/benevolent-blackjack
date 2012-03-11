# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

inherit distutils

DESCRIPTION="Console-based Blackjack program that supports some advanced features and training."
HOMEPAGE="http://www.qnan.org/~pmw/software/bbj"
SRC_URI="http://www.qnan.org/~pmw/software/${PN}/releases/${P}.tar.bz2"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE=""

RDEPEND=">=dev-python/peafowlterm-1.0"

S=${WORKDIR}/${PN}

DOCS="CHANGES THANKS TODO"

src_install() {
	distutils_src_install
	doman doc/${PN}.6 || die "Could not set up the manpage."
}
