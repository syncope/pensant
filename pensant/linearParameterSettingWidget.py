# Copyright (C) 2018-9  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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
import numpy as np


class LinearParameterSettingWidget(parameterSettingWidget.ParameterSettingWidget):

    def __init__(self, model, xdata, ydata, **kw):
        super(LinearParameterSettingWidget, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.interceptSlider.valueChanged.connect(self._interceptScaler)
        self.slopeSlider.valueChanged.connect(self._slopeScaler)
        self._modelprefix = str("m" + str(self._name) + "_")
        self._model = model
        self._exo.setName(self._modelprefix)
        self._setColour(self._exo.colour())
        self.useLBSlope.hide()
        self.useUBSlope.hide()
        self.slopeLBValue.hide()
        self.slopeUBValue.hide()
        self.useLBIntercept.hide()
        self.useUBIntercept.hide()
        self.interceptLBValue.hide()
        self.interceptUBValue.hide()
        self.extendButton.clicked.connect(self._togglehide)
        self.chooseColourButton.clicked.connect(self._chooseColour)

    def _togglehide(self):
        if self.useLBSlope.isHidden():
            self.useLBSlope.show()
            self.useUBSlope.show()
            self.slopeLBValue.show()
            self.slopeUBValue.show()
            self.useLBIntercept.show()
            self.useUBIntercept.show()
            self.interceptLBValue.show()
            self.interceptUBValue.show()
            self.extendButton.setText("Shorten")
        else:
            self.useLBSlope.hide()
            self.useUBSlope.hide()
            self.slopeLBValue.hide()
            self.slopeUBValue.hide()
            self.useLBIntercept.hide()
            self.useUBIntercept.hide()
            self.interceptLBValue.hide()
            self.interceptUBValue.hide()
            self.extendButton.setText("Extend")

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # first basic calculations
        self._slopeDisplay = float(np.mean(self._ydata))/float(np.mean(self._xdata))
        self._slopeBounds = (-10*self._slopeDisplay, 10*self._slopeDisplay)
        self._interceptDisplay = 0.
        self._interceptBounds = (-1*float(np.amax(self._ydata)), float(np.amax(self._ydata)))

        # now set initial values
        self.slopeValue.setValue(self._slopeDisplay)
        self.interceptValue.setValue(self._interceptDisplay)

        # and now the boundaries -- as valid for the slider
        # slope:
        self.slopeLBValue.setValue(self._slopeBounds[0])
        self.slopeUBValue.setValue(self._slopeBounds[1])
        # intercept
        self.interceptLBValue.setValue(self._interceptBounds[0])
        self.interceptUBValue.setValue(self._interceptBounds[1])

        self.updateFit.emit()

    def _interceptScaler(self, val):
        valuewidth = self.interceptUBValue.value() - self.interceptLBValue.value()
        currentVal = (self.interceptSlider.minimum() + val * self.interceptSlider.singleStep())/(self.interceptSlider.maximum() - self.interceptSlider.minimum())
        self.interceptValue.setValue(self.interceptLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def _slopeScaler(self, val):
        valuewidth = self.slopeUBValue.value() - self.slopeLBValue.value()
        currentVal = (self.slopeSlider.minimum() + val * self.slopeSlider.singleStep())/(self.slopeSlider.maximum() - self.slopeSlider.minimum())
        self.slopeValue.setValue(self.slopeLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(intercept=self.interceptValue.value(), slope=self.slopeValue.value())
        self._exo.setData(self._model.eval(self._parameters, x=self._xdata))
        return self._exo

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = {self._modelprefix:
                 {'modeltype': 'linearModel',
                  'intercept': {'value': self.interceptValue.value(), 'vary': (not self.interceptFixedCB.isChecked())},
                  'slope': {'value': self.slopeValue.value(), 'vary': (not self.slopeFixedCB.isChecked())},
                  }
                 }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model

    def _chooseColour(self):
        self._qcd = QtGui.QColorDialog()
        self._qcd.show()
        self._qcd.currentColorChanged.connect(self._setColour)

    def _setColour(self, colour):
        self.setColour(colour)
        self.colourDisplay.setStyleSheet(("background-color:"+str(colour.name())))
        self.updateFit.emit()
