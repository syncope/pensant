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

from . import parameterSettingDialog
import numpy as np
import math


class shiftedexponentialParameterSettingDialog(parameterSettingDialog.ParameterSettingDialog):

    # shifted exponential: 'amp*exp(-lambda*(x-x0))-offset'

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(shiftedexponentialParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.ampSlider.valueChanged.connect(self._ampScaler)
        self.lSlider.valueChanged.connect(self._lScaler)
        self.offSlider.valueChanged.connect(self._offScaler)
        self.xzeroSlider.valueChanged.connect(self._xzeroScaler)
        self._modelName = modelname
        self._model = model
        self._model.prefix = "m" + str(self._index) + "_"
        self._parameters = None
        self.guessStartValuesBtn.clicked.connect(print)
        self.guessStartValuesBtn.hide()
        self.configDonePushBtn.clicked.connect(self._guessingDone)
        self.extendButton.clicked.connect(self._togglehide)
        self.chooseColourButton.clicked.connect(self._chooseColour)

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # take care of amp, lambda (l), offset (off) and x0 (xzero)
        # first basic calculations
        self._aDisplay = float(np.mean(self._ydata))
        self._aBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))
        self._tauDisplay = float(np.mean(self._ydata))/float(np.mean(self._xdata))
        self._tauBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))

        # first fix the accuracy of the display
        # number of steps;
        aStep = (self._aBounds[1] - self._aBounds[0])/(self.aSlider.maximum()-self.aSlider.minimum())
        aAcc = math.floor(math.fabs(math.log10(aStep)))+2
        self.aValue.setDecimals(aAcc)
        self.aLBValue.setDecimals(aAcc)
        self.aUBValue.setDecimals(aAcc)

        tauStep = (self._tauBounds[1] - self._tauBounds[0])/(self.tauSlider.maximum()-self.tauSlider.minimum())
        tauAcc = math.floor(math.fabs(math.log10(tauStep)))+2
        self.tauValue.setDecimals(tauAcc)
        self.tauLBValue.setDecimals(tauAcc)
        self.tauUBValue.setDecimals(tauAcc)

        # now set initial values
        self.aValue.setValue(self._aDisplay)
        self.tauValue.setValue(self._tauDisplay)

        # and now the boundaries -- as valid for the slider
        # a
        self.aLBValue.setValue(self._aBounds[0])
        self.aUBValue.setValue(self._aBounds[1])
        # tau
        self.tauLBValue.setValue(self._tauBounds[0])
        self.tauUBValue.setValue(self._tauBounds[1])

        self.updateFit.emit()

    def _aScaler(self, val):
        valuewidth = self._aBounds[1]-self._aBounds[0]
        currentVal = (self.aSlider.minimum() + float(val * self.aSlider.singleStep()))/(self.aSlider.maximum() - self.aSlider.minimum())
        self.aValue.setValue(self._aBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _tauScaler(self, val):
        valuewidth = self._tauBounds[1]-self._tauBounds[0]
        currentVal = (self.tauSlider.minimum() + float(val * self.tauSlider.singleStep()))/(self.tauSlider.maximum() - self.tauSlider.minimum())
        self.tauValue.setValue(self._tauBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(a=self.aValue.value(), tau=self.tauValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = {self._model.prefix:
                 {'modeltype': 'shiftedexponentialModel',
                  'a': {'value': self.aValue.value(), 'vary': (not self.aFixedCB.isChecked())},
                  'tau': {'value': self.tauValue.value(), 'vary': (not self.tauFixedCB.isChecked())},
                  }
                 }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model
