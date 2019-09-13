# Copyright (C) 2018  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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

from PyQt4 import QtCore, QtGui, uic


class ParameterSettingWidget(QtGui.QWidget):
    updateFit = QtCore.pyqtSignal()
    guessingDone = QtCore.pyqtSignal()

    def __init__(self, uifile, name='0', parent=None):
        super(ParameterSettingWidget, self).__init__(parent)
        uic.loadUi(uifile, self)
        self._name = name
        self._exo = fitExchangeObject(name = name)

    def passData(self, xdata, ydata):
        self._xdata = xdata
        self._ydata = ydata
        self.update()
        self._exo.setData(ydata)

    def update(self):
        pass

    def getName(self):
        return self._name

    def colour(self):
        return self._exo.colour()

    def setColour(self, colour):
        self._exo.setColour(colour)


class guiParameter():

    def __init__(self, val=None, lowlim=None, uplim=None):
        self.lowerLimit = lowlim
        self.upperLimit = uplim
        self.currentValue = val
        self.check()

    def setLimits(self, lowlim, uplim):
        self.setLowerLimit(lowlim)
        self.setUpperLimit(uplim)

    def setLowerLimit(self, lowlim):
        self.lowerLimit = lowlim
        if self.currentValue < lowlim:
            self.currentValue = lowlim

    def setUpperLimit(self, uplim):
        self.upperLimit = uplim
        if self.currentValue > uplim:
            self.currentValue = uplim

    def check(self):
        if self.currentValue > self.upperLimit:
            self.currentValue = self.upperLimit
        elif self.currentValue < self.lowerLimit:
            self.currentValue = self.lowerLimit

class fitExchangeObject():

    def __init__(self, data=None, name=None, colour=None):
        self._data = data
        self._name = name
        self._colour = colour

    def data(self):
        return self._data

    def name(self):
        return self._name

    def colour(self):
        return self._colour

    def set(self, data, name, colour):
        self._data = data
        self._name = name
        self._colour = colour

    def setData(self, data):
        self._data = data

    def setName(self, name):
        self._name = name

    def setColour(self, colour):
        self._colour = colour

    def dump(self):
        print("i am " + str(self._data) + " and " + str(self._colour))
