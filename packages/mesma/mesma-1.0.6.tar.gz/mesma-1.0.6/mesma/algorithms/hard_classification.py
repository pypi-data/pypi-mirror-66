# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : February 2019
| Copyright           : © 2019 - 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
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

from mesma.algorithms.shade_normalisation import ShadeNormalisation


class HardClassification:
    """
    Do a simple hard classification on an existing MESMA fraction image.
    """

    def __init__(self):
        pass

    @staticmethod
    def execute(mesma_fraction_image: np.array, shade_band: int = -1) -> np.array:
        """
        Execute the hard classification. The return value single band image indicating the dominant class.

        :param mesma_fraction_image: Fraction image of the output of the MESMA algorithm.
        :param shade_band: Band number with the shade fraction (set to None in case no shade band given).
        :return: Hard classified image with values reflecting the dominant band.
        """

        normalized_image = ShadeNormalisation().execute(mesma_fraction_image, shade_band)
        classified_image = np.int16(np.argmax(normalized_image, axis=0))
        return classified_image
