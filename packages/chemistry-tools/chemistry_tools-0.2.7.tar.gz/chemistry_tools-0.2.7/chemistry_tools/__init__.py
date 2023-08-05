#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  assay, Atom, Bond, Compound, Constants, Errors, Lookup, Substance and
#  Utils based on PubChemPy by Matt Swain <m.swain@me.com>
#  Available under the MIT License
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

__author__ = "Dominic Davis-Foster"
__copyright__ = "2019-2020 Dominic Davis-Foster"

__license__ = "LGPL"
__version__ = "0.2.7"
__email__ = "dominic@davis-foster.co.uk"


# stdlib
import pathlib

# 3rd party
import appdirs
import requests_cache

cache_dir = pathlib.Path(appdirs.user_cache_dir("chemistry_tools"))
if not cache_dir.exists():
	cache_dir.mkdir(parents=True, exist_ok=True)

# Setup Cache and keep for ~ a month
requests_cache.install_cache(str(cache_dir / "chemistry_tools_cache"), expire_after=2500000)


from . import assay
from . import atom
from . import bond
from . import compound
from . import constants
from . import errors
from . import lookup
from . import property_format
from . import spectrum_similarity
from . import substance
from . import toxnet
from . import utils
from . import cas


def clear_cache():
	requests_cache.clear()


__all__ = [
		"spectrum_similarity",
		"assay",
		"atom",
		"bond",
		"compound",
		"constants",
		"errors",
		"property_format",
		"substance",
		"toxnet",
		"utils",
		]

if __name__ == '__main__':
	print(__version__)

