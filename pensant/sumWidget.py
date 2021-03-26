# Copyright (C) 2019  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
# email contact: christoph.rosemann@desy.de
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation in  version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

from . import parameterSettingWidget
from PyQt4 import QtGui


class SumWidget(parameterSettingWidget.ParameterSettingWidget):

    def __init__(self, model, xdata, ydata, **kw):
        super(SumWidget, self).__init__(**kw)
        self.passData(xdata, ydata)
        self._setColour(self._exo.colour())
        self.chooseColourButton.clicked.connect(self._chooseColour)

    def update(self):
        self.updateFit.emit()

    def getCurrentFitData(self):
        return self._exo

    def getName(self):
        return self._modelName

    def _chooseColour(self):
        self._qcd = QtGui.QColorDialog()
        self._qcd.show()
        self._qcd.colorSelected.connect(self._setColour)

    def _setColour(self, colour):
        self.setColour(colour)
        self.chooseColourButton.setStyleSheet(("background-color:"+str(colour.name())))
