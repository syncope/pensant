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


class ParameterSettingDialog(QtGui.QDialog):
    updateFit = QtCore.pyqtSignal()
    guessingDone = QtCore.pyqtSignal()

    def __init__(self, uifile, index=None, parent=None):
        super(ParameterSettingDialog, self).__init__(parent)
        uic.loadUi(uifile, self)
        self._index = index

    def passData(self, xdata, ydata):
        self._xdata = xdata
        self._ydata = ydata
        self.update()

    def update(self):
        pass

    def getIndex(self):
        return self._index


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
