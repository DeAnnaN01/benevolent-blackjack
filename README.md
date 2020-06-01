Have you ever wanted to be a Las Vegas high roller?
===================================================

Look no further than Benevolent Blackjack, your pocket pal that'll guide you to untold riches.

Benevolent Blackjack is a cross-platform console-based program that plays a [game of Blackjack](https://en.wikipedia.org/wiki/Blackjack) with you, acting as the dealer and (optionally) any number of co-players.
In addition to being able to play the role of an apathetic dealer, Benevolent Blackjack has two unique features: it can benevolently advise you on whether you are [making optimal decisions](https://en.wikipedia.org/wiki/Blackjack#Basic_strategy) to minimize the house edge, and it can train you to count cards.

Once you become a master at winning Blackjack with this program, all that's left is to charter a private airplane to McCarran International Airport!

![Screenshot on macOS](./doc/screenshot.png)

Features
========

* BBJ supports a configurable number of artificial co-players at your table.
* BBJ has flexible table rules.  It can enforce rules about a table minimum and maximum, doubling down, surrender, doubling after split, and hitting split Aces.  You can configure the number of decks, the Blackjack payout ratio, whether the dealer hits on soft 17, and whether Five-Card Charlie is enabled.
* BBJ supports insurance.
* BBJ supports simple peaceful gameplay, without worrying about making optimal decisions.
* BBJ can advise you when you fail to follow basic strategy.
* BBJ can train you to count cards accurately.
* BBJ is cross-platform, thanks to Python.
* BBJ is console-based.  This has many advantages.  BBJ does not rely on any graphical toolkit, any window system, or even on having a mouse.  It can be played over Telnet or SSH.
* BBJ uses terminal colors.  You can set coloring suitable for a dark background, suitable for a light background, or disable coloring.

Installing and running
======================

I wish all computers would come with Benevolent Blackjack by default, but til then, you can install this game from [PyPI](https://pypi.org/project/Benevolent-Blackjack/).

Using the command line,

    pip install Benevolent-Blackjack

Then run like so for regular peaceful gameplay:

    bbj

Or, to be told when you made a bad move:

    bbj --benevolent

If those commands do not work on your system, try one of these instead:

    python -m bbj
    python -m bbj --benevolent

For more options, see `bbj --help`.

Developing
==========

Did you win big, retire, and want to dabble in software development from your new Florida estate?
Be my guest and make some contributions.

This software was developed without any unit tests; I am sorry about that.
At the time I wrote it, I was in college and had never written a single unit test.
All testing was passionately manual.

The software almost certainly does not follow best Python practices, too.
All improvements are very welcome!

The documentation for Benevolent Blackjack is in several places:

* the doc/ directory
* the manpage;
* the source code is reasonably well commented.

Releasing:

1. Update `bbj/metadata.py` version number to a [developmental release](https://www.python.org/dev/peps/pep-0440/#developmental-releases)
2. Package and upload to test.pypi.org:

    $ rm -rf build dist
    $ python3 setup.py sdist bdist_wheel
    $ python3 -m twine upload --repository Benevolent-Blackjack-test dist/*

3. Test on all supported platforms:

    $ pip install --pre --upgrade --index-url https://test.pypi.org/simple Benevolent-Blackjack
    $ python -m bbj

4. Update version number to a final release number.
5. Re-package and upload to pypi.org.

Thanks
======

Thanks to Andreas Schagerer for extensively testing the program, reporting many issues, and suggesting new features.
  
TODO
====

* Implement the option of using a continuous shuffler.
* Separate the UI from the Blackjack 'engine'.
* Add unit tests
* Fix console colors in Windows 10 Command Prompt
* Rewrite peafowlterm to not reinvent the linked list
* Make imports more consistent and coherent (`bbj.BJSeqOutcome.BJSeqOutcome` etc.)

Lastly
======

If you win money thanks to Benevolent Blackjack, I accept donations of cash, stock, and real estate.
