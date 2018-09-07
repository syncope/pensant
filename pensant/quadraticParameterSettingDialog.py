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

from . import parameterSettingDialog
import numpy as np
import math


class QuadraticParameterSettingDialog(parameterSettingDialog.ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(QuadraticParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.aSlider.valueChanged.connect(self._aScaler)
        self.bSlider.valueChanged.connect(self._bScaler)
        self.cSlider.valueChanged.connect(self._cScaler)
        self._modelName = modelname
        self._model = model
        self._model.prefix = "m" + str(self._index) + "_"
        self._parameters = None
        self.guessStartValuesBtn.clicked.connect(print)
        self.configDonePushBtn.clicked.connect(self._guessingDone)

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # first basic calculations
        self._aDisplay = float(np.mean(self._ydata))
        self._aBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))
        self._bDisplay = float(np.mean(self._ydata))/float(np.mean(self._xdata))
        self._bBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))
        self._cDisplay = float(np.mean(self._ydata))/math.sqrt(np.mean(self._xdata))
        self._cBounds = (-10.*float(self._cDisplay), 10.*float(self._cDisplay))

        # first fix the accuracy of the display
        # number of steps;
        aStep = (self._aBounds[1] - self._aBounds[0])/(self.aSlider.maximum()-self.aSlider.minimum())
        aAcc = math.floor(math.fabs(math.log10(aStep)))+2
        self.aValue.setDecimals(aAcc)
        self.aLBValue.setDecimals(aAcc)
        self.aUBValue.setDecimals(aAcc)

        bStep = (self._bBounds[1] - self._bBounds[0])/(self.bSlider.maximum()-self.bSlider.minimum())
        bAcc = math.floor(math.fabs(math.log10(bStep)))+2
        self.bValue.setDecimals(bAcc)
        self.bLBValue.setDecimals(bAcc)
        self.bUBValue.setDecimals(bAcc)

        cStep = (self._cBounds[1] - self._cBounds[0])/(self.cSlider.maximum()-self.cSlider.minimum())
        cAcc = math.floor(math.fabs(math.log10(cStep)))+2
        self.cValue.setDecimals(cAcc)
        self.cLBValue.setDecimals(cAcc)
        self.cUBValue.setDecimals(cAcc)

        # now set initial values
        self.aValue.setValue(self._aDisplay)
        self.bValue.setValue(self._bDisplay)
        self.cValue.setValue(self._cDisplay)

        # and now the boundaries -- as valid for the slider
        # a:
        self.aLBValue.setValue(self._aBounds[0])
        self.aUBValue.setValue(self._aBounds[1])
        # b
        self.bLBValue.setValue(self._bBounds[0])
        self.bUBValue.setValue(self._bBounds[1])
        # c
        self.cLBValue.setValue(self._cBounds[0])
        self.cUBValue.setValue(self._cBounds[1])

        self.updateFit.emit()

    def _aScaler(self, val):
        valuewidth = self._aBounds[1]-self._aBounds[0]
        currentVal = (self.aSlider.minimum() + float(val * self.aSlider.singleStep()))/(self.aSlider.maximum() - self.aSlider.minimum())
        self.aValue.setValue(self._aBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _bScaler(self, val):
        valuewidth = self._bBounds[1]-self._bBounds[0]
        currentVal = (self.bSlider.minimum() + float(val * self.bSlider.singleStep()))/(self.bSlider.maximum() - self.bSlider.minimum())
        self.bValue.setValue(self._bBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _cScaler(self, val):
        valuewidth = self._cBounds[1]-self._cBounds[0]
        currentVal = (self.cSlider.minimum() + float(val * self.cSlider.singleStep()))/(self.cSlider.maximum() - self.cSlider.minimum())
        self.cValue.setValue(self._cBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(a=self.aValue.value(), b=self.bValue.value(), c=self.cValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = {self._model.prefix:
                 {'modeltype': 'quadraticModel',
                  'a': {'value': self.aValue.value(), 'vary': (not self.aFixedCB.isChecked())},
                  'b': {'value': self.bValue.value(), 'vary': (not self.bFixedCB.isChecked())},
                  'c': {'value': self.cValue.value(), 'vary': (not self.cFixedCB.isChecked())}
                  }
                 }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model
