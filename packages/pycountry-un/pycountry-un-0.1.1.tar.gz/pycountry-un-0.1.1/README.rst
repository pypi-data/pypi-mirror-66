============
Pycountry-UN
============

A simple package that provides lists of countries in the United Nation's World Economic Situation
and Prospects as sequences of Pycountry elements.

Usage
=====

First, you need to install it using ``pip install pycountry-un`` or your method of choice.
Secondly, just import it and load the lists

>>> import pycountry_un as un
>>> un.upper_middle_income_countries.lookup("Brazil")
Country(alpha_2='BR', alpha_3='BRA', name='Brazil', numeric='076', official_name='Federative Republic of Brazil')


Observation
===========

If you disagree with any of these classifications, address you concerns to the United Nations.
This package only accepts changes to reflect the most current understanding published on the
official UN's `World Economic Situation and Prospects <https://www.un.org/development/desa/dpad/wp-content/uploads/sites/45/WESP2020_FullReport.pdf>`_.
Patches will only be accepted concerning discrepancies with that publication.
