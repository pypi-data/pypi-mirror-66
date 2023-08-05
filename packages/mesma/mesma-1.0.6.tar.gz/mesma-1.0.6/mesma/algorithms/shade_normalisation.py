# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : September 2018
| Copyright           : © 2018 - 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from VIPER Tools 2.0 (UC Santa Barbara, VIPER Lab).
|                       Dar Roberts, Kerry Halligan, Philip Dennison, Kenneth Dudley, Ben Somers, Ann Crabbé
|
| This file is part of the QGIS Neural Network MLP Classifier plugin and mlp-image-classifier python package.
|
| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
| License as published by the Free Software Foundation, either version 3 of the License, or any later version.
|
| This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
| warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License along with Foobar.  If not see www.gnu.org/licenses.
| ----------------------------------------------------------------------------------------------------------------------
"""
import numpy as np


class ShadeNormalisation:
    """
    Do a simple shade normalization on an existing MESMA fraction image: the shade fraction is removed and the other
    fractions are normalized to sum to one.
    """

    def __init__(self):
        pass

    @staticmethod
    def execute(mesma_fraction_image: np.array, shade_band: int = -1) -> np.array:
        """
        Execute shade normalisation. The return value is a normalized fraction image, with one band less as the input.

        :param mesma_fraction_image: Fraction image of the output of the MESMA algorithm.
        :param shade_band: Band number with the shade fraction (set to None in case no shade band given).
        :return: Normalised fraction image.
        """

        n_bands = len(mesma_fraction_image)

        if mesma_fraction_image.ndim <= 2 or n_bands < 3:
            raise Exception('MESMA Fractions Image must have at least 3 bands (i.e. based on at least 3-EM models)')

        non_shade_bands = list(range(n_bands))
        if shade_band is not None:
            non_shade_bands.pop(shade_band)

        with np.errstate(divide='ignore', invalid='ignore'):
            new_fraction_image = mesma_fraction_image[non_shade_bands] / \
                                 np.sum(mesma_fraction_image[non_shade_bands], axis=0)[np.newaxis, :, :]
            new_fraction_image[np.isnan(new_fraction_image)] = 0

        return new_fraction_image
