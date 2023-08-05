# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------|
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
import os
import argparse

from mesma.algorithms.hard_classification import HardClassification
from mesma.io.imports import import_band_names
from mesma.io.operators import HardClassificationOperator, CLIProgressBar
from mesma.external.hubdc.applier import Applier, ApplierInputRaster, ApplierOutputRaster


def create_parser():
    """ The parser for the CLI command parameters. """
    parser = argparse.ArgumentParser(description=str(HardClassification.__doc__))

    # image
    parser.add_argument('image', metavar='fraction image',
                        help='the mesma output image ending on _fractions')

    # output
    parser.add_argument('-o', '--output', metavar='\b',
                        help="output image file (default: in same folder with extension '_classification')")

    return parser


def run_hard_classification(args):
    """
    Documentation: mesma-classify -h
    """

    # Shade band present?
    band_names, shade_band_index = import_band_names(args.image)

    # Get output name
    if args.output is None:
        basename, extension = os.path.splitext(args.image)
        output = basename + '_classification' + extension
    else:
        output = args.output

    # set up the applier
    applier = Applier()
    applier.controls.setProgressBar(CLIProgressBar())
    applier.inputRaster.setRaster(key='raster', value=ApplierInputRaster(filename=args.image))
    applier.outputRaster.setRaster(key='classification', value=ApplierOutputRaster(filename=output))

    # apply shade normalisation
    applier.apply(operatorType=HardClassificationOperator, band_names=band_names, shade_band=shade_band_index)
    print("Done.")


def main():
    """ Function called by CLI. """
    parser = create_parser()
    run_hard_classification(parser.parse_args())
