#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = '0.0.1'

from .top_level import ColorSpaceConverter
from .top_level import GryConverter
from .top_level import HsvConverter
from .top_level import LabConverter
from .top_level import LmsConverter
from .top_level import XyzConverter
from .top_level import YuvConverter
from .converter_baseclass import ConverterBaseclass
