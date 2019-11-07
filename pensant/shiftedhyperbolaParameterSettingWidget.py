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
import numpy as np


class shiftedhyperbolaParameterSettingWidget(parameterSettingWidget.ParameterSettingWidget):

    def __init__(self, model, xdata, ydata, **kw):
        super(shiftedhyperbolaParameterSettingWidget, self).__init__(**kw)
        self.passData(xdata, ydata)

        self.aSlider.valueChanged.connect(self._aScaler)
        self.xzeroSlider.valueChanged.connect(self._xzeroScaler)
        self._modelprefix = str("m" + str(self._name) + "_")
        self._model = model
        self._exo.setName(self._modelprefix)
        self._setColour(self._exo.colour())
        self._parameters = None
        self.useLBA.hide()
        self.useUBA.hide()
        self.aLBValue.hide()
        self.aUBValue.hide()
        self.useLBxzero.hide()
        self.useUBxzero.hide()
        self.xzeroLBValue.hide()
        self.xzeroUBValue.hide()
        self.extendButton.clicked.connect(self._togglehide)
        self.chooseColourButton.clicked.connect(self._chooseColour)

    def _togglehide(self):
        if self.useLBA.isHidden():
            self.useLBA.show()
            self.useUBA.show()
            self.aLBValue.show()
            self.aUBValue.show()
            self.useLBxzero.show()
            self.useUBxzero.show()
            self.xzeroLBValue.show()
            self.xzeroUBValue.show()
            self.extendButton.setText("Shorten")
        else:
            self.useLBA.hide()
            self.useUBA.hide()
            self.aLBValue.hide()
            self.aUBValue.hide()
            self.useLBxzero.hide()
            self.useUBxzero.hide()
            self.xzeroLBValue.hide()
            self.xzeroUBValue.hide()
            self.extendButton.setText("Extend")

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # first basic calculations
        self._xzeroDisplay = float(self._xdata[0])
        self._xzeroBounds = (0., 2*self._xzeroDisplay)
        self._aDisplay = 1.
        self._aBounds = (0., 2*float(np.amax(self._ydata)))

        # now set initial values
        self.xzeroValue.setValue(self._xzeroDisplay)
        self.aValue.setValue(self._aDisplay)

        # and now the boundaries -- as valid for the slider
        # xzero:
        self.xzeroLBValue.setValue(self._xzeroBounds[0])
        self.xzeroUBValue.setValue(self._xzeroBounds[1])
        # a
        self.aLBValue.setValue(self._aBounds[0])
        self.aUBValue.setValue(self._aBounds[1])

        self.updateFit.emit()

    def _aScaler(self, val):
        valuewidth = self.aUBValue.value() - self.aLBValue.value()
        currentVal = (self.aSlider.minimum() + val * self.aSlider.singleStep())/(self.aSlider.maximum() - self.aSlider.minimum())
        self.aValue.setValue(self.aLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def _xzeroScaler(self, val):
        valuewidth = self.xzeroUBValue.value() - self.xzeroLBValue.value()
        currentVal = (self.xzeroSlider.minimum() + val * self.xzeroSlider.singleStep())/(self.xzeroSlider.maximum() - self.xzeroSlider.minimum())
        self.xzeroValue.setValue(self.xzeroLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(a=self.aValue.value(), xzero=self.xzeroValue.value())
        self._exo.setData(self._model.eval(self._parameters, x=self._xdata))
        return self._exo

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = {self._model.prefix:
                 {'modeltype': 'shiftedhyperbolaModel',
                  'a': {'value': self.aValue.value(), 'vary': (not self.aFixedCB.isChecked())},
                  'xzero': {'value': self.xzeroValue.value(), 'vary': (not self.xzeroFixedCB.isChecked())},
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
