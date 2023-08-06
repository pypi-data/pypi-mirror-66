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

import numpy as np

from color_space_converter.converter_baseclass import ConverterBaseclass
from color_space_converter.xyz_converter import XyzConverter

# Observer. = 2°, Illuminant = D65 (from Adobe)
REF_X = 95.047
REF_Y = 100.000
REF_Z = 108.883


class LabConverter(XyzConverter, ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        super(LabConverter, self).__init__(*args, **kwargs)

    def rgb2lab(self, rgb: np.ndarray = None) -> np.ndarray:
        """ Convert RGB color space to Lab color space

        :param rgb: input array in red, green and blue (RGB) space
        :type rgb: :class:`~numpy:numpy.ndarray`
        :return: array in Lab space
        :rtype: ~numpy:np.ndarray

        """

        # override if input array is provided
        self._arr = rgb if rgb is not None else self._arr

        xyz = self.rgb2xyz(rgb)
        lab = self.xyz2lab(xyz)

        return lab

    def lab2rgb(self, lab: np.ndarray = None) -> np.ndarray:
        """ Convert Lab color space to RGB color space

        :param lab: input array in Lab space
        :type lab: :class:`~numpy:numpy.ndarray`
        :return: array in red, green and blue (RGB) space
        :rtype: ~numpy:np.ndarray

        """

        # override if input array is provided
        self._arr = lab if lab is not None else self._arr

        xyz = self.lab2xyz(lab)
        rgb = self.xyz2rgb(xyz)

        return rgb

    def lab_conv(self, img: np.ndarray = None, inverse: bool = False) -> np.ndarray:
        """ Convert RGB color space to Lab color space or vice versa given the inverse option.

        :param img: input array in either RGB or Lab color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param inverse: option that determines whether conversion is from rgb2lab (False) or lab2rgb (True)
        :type inverse: :class:`boolean`
        :return: color space converted array
        :rtype: ~numpy:np.ndarray

        """

        # override if inputs present
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv

        if not self._inv:
            arr = self.rgb2lab(self._arr)
        else:
            arr = self.lab2rgb(self._arr)

        return arr

    def xyz2lab(self, xyz: np.ndarray = None) -> np.ndarray:
        """ Convert xyz color space to Lab color space

        :param xyz: input array in xyz space
        :type xyz: :class:`~numpy:numpy.ndarray`
        :return: array in Lab space
        :rtype: ~numpy:np.ndarray

        """

        xyz[..., 0] /= REF_X
        xyz[..., 1] /= REF_Y
        xyz[..., 2] /= REF_Z

        for ch in range(xyz.shape[2]):
            mask = xyz[..., ch] > 0.008856
            xyz[..., ch][mask] = np.power(xyz[..., ch], 1 / 3.)[mask]
            xyz[..., ch][~mask] = (7.787 * xyz[..., ch] + 16 / 116.)[~mask]

        lab = np.zeros(xyz.shape)
        lab[..., 0] = (116 * xyz[..., 1]) - 16
        lab[..., 1] = 500 * (xyz[..., 0] - xyz[..., 1])
        lab[..., 2] = 200 * (xyz[..., 1] - xyz[..., 2])

        return lab

    def lab2xyz(self, lab: np.ndarray = None) -> np.ndarray:
        """ Convert Lab color space to RGB color space

        :param lab: input array in Lab space
        :type lab: :class:`~numpy:numpy.ndarray`
        :return: array in red, green and blue (RGB) space
        :rtype: ~numpy:np.ndarray

        """

        xyz = np.zeros(lab.shape)
        xyz[..., 1] = (lab[..., 0] + 16) / 116.
        xyz[..., 0] = lab[..., 1] / 500. + xyz[..., 1]
        xyz[..., 2] = xyz[..., 1] - lab[..., 2] / 200.

        for ch in range(xyz.shape[2]):
            mask = np.power(xyz[..., ch], 3) > 0.008856
            xyz[..., ch][mask] = np.power(xyz[..., ch], 3)[mask]
            xyz[..., ch][~mask] = (xyz[..., ch] - 16 / 116.)[~mask] / 7.787

        xyz[..., 0] *= REF_X
        xyz[..., 1] *= REF_Y
        xyz[..., 2] *= REF_Z

        return xyz
