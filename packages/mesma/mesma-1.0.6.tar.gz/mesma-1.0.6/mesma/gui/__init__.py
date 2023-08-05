# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : March 2020
| Copyright           : © 2020 by Ann Crabbé (KU Leuven)
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
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QWidget, QLabel, QHBoxLayout
from mesma.resources_rc import qInitResources
qInitResources()


class LogoWidget(QWidget):
    """ QWidget with the project's logo. To be placed above each widget/dialog. """

    def __init__(self, parent=None):
        super(LogoWidget, self).__init__(parent=parent)

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignHCenter)

        lumos = QLabel(self)
        lumos.setPixmap(QPixmap(':/lumos_full'))
        layout.addWidget(lumos)

        viper = QLabel(self)
        viper.setPixmap(QPixmap(':/viper_full'))
        layout.addWidget(viper)


class EmittingStream:
    """ QObject to catch the terminal output and send it along with pyqtSignal. """

    def __init__(self, tab_widget):

        self.tab_widget = tab_widget
        self.log_index = tab_widget.indexOf(tab_widget.findChild(QWidget, 'tab_log'))
        self.log_widget = tab_widget.findChild(QWidget, 'logBrowser')

    def write(self, text):
        text = str(text)
        self.log_widget.append(text)
        self.tab_widget.setCurrentIndex(self.log_index)
