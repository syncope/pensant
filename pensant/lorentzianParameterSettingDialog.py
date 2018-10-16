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


class LorentzianParameterSettingDialog(parameterSettingDialog.ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(LorentzianParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.centerSlider.valueChanged.connect(self._centerScaler)
        self.amplitudeSlider.valueChanged.connect(self._ampScaler)
        self.sigmaSlider.valueChanged.connect(self._sigmaScaler)
        self._modelName = modelname
        self._model = model
        self._model.prefix = "m" + str(self._index) + "_"
        self._parameters = None
        self.guessStartValuesBtn.clicked.connect(print)
        self.guessStartValuesBtn.hide()
        self.configDonePushBtn.clicked.connect(self._guessingDone)

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # first basic calculations
        self._centerDisplay = float(np.mean(self._xdata))
        self._centerBounds = (float(np.amin(self._xdata)), float(np.amax(self._xdata)))
        self._sigmaDisplay = float(np.amax(self._xdata) - np.amin(self._xdata))/10.
        self._sigmaBounds = (float(self._sigmaDisplay/10.), float(self._sigmaDisplay*2.))
        self._amplitudeDisplay = float(np.amax(self._ydata))/8.
        self._amplitudeBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))

        # first fix the accuracy of the display
        # number of steps;
        centerStep = (self._centerBounds[1] - self._centerBounds[0])/(self.centerSlider.maximum()-self.centerSlider.minimum())
        centerAcc = math.floor(math.fabs(math.log10(centerStep)))+2
        self.centerValue.setDecimals(centerAcc)
        self.centerLBValue.setDecimals(centerAcc)
        self.centerUBValue.setDecimals(centerAcc)

        amplitudeStep = (self._amplitudeBounds[1] - self._amplitudeBounds[0])/(self.amplitudeSlider.maximum()-self.amplitudeSlider.minimum())
        amplitudeAcc = math.floor(math.fabs(math.log10(amplitudeStep)))+2
        self.amplitudeValue.setDecimals(amplitudeAcc)
        self.amplitudeLBValue.setDecimals(amplitudeAcc)
        self.amplitudeUBValue.setDecimals(amplitudeAcc)

        sigmaStep = (self._sigmaBounds[1] - self._sigmaBounds[0])/(self.sigmaSlider.maximum()-self.sigmaSlider.minimum())
        sigmaAcc = math.floor(math.fabs(math.log10(sigmaStep)))+2
        self.sigmaValue.setDecimals(sigmaAcc)
        self.sigmaLBValue.setDecimals(sigmaAcc)
        self.sigmaUBValue.setDecimals(sigmaAcc)

        # now set initial values
        self.centerValue.setValue(self._centerDisplay)
        self.amplitudeValue.setValue(self._amplitudeDisplay)
        self.sigmaValue.setValue(self._sigmaDisplay)

        # and now the boundaries -- as valid for the slider
        # center:
        self.centerLBValue.setValue(self._centerBounds[0])
        self.centerUBValue.setValue(self._centerBounds[1])
        # amplitude
        self.amplitudeLBValue.setValue(self._amplitudeBounds[0])
        self.amplitudeUBValue.setValue(self._amplitudeBounds[1])
        # sigma
        self.sigmaLBValue.setValue(self._sigmaBounds[0])
        self.sigmaUBValue.setValue(self._sigmaBounds[1])

        self.updateFit.emit()

    def _centerScaler(self, val):
        valuewidth = self._centerBounds[1]-self._centerBounds[0]
        currentVal = (self.centerSlider.minimum() + float(val * self.centerSlider.singleStep()))/(self.centerSlider.maximum() - self.centerSlider.minimum())
        self.centerValue.setValue(self._centerBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _ampScaler(self, val):
        valuewidth = self.amplitudeUBValue.value() - self.amplitudeLBValue.value()
        currentVal = (self.amplitudeSlider.minimum() + val * self.amplitudeSlider.singleStep())/(self.amplitudeSlider.maximum() - self.amplitudeSlider.minimum())
        self.amplitudeValue.setValue(self.amplitudeLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def _sigmaScaler(self, val):
        valuewidth = self.sigmaUBValue.value() - self.sigmaLBValue.value()
        currentVal = (self.sigmaSlider.minimum() + float(val * self.sigmaSlider.singleStep()))/(self.sigmaSlider.maximum() - self.sigmaSlider.minimum())
        self.sigmaValue.setValue(self.sigmaLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(center=self.centerValue.value(), amplitude=self.amplitudeValue.value(), sigma=self.sigmaValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = {self._model.prefix:
                 {'modeltype': 'lorentzianModel',
                  'center': {'value': self.centerValue.value(), 'vary': (not self.centerFixedCB.isChecked())},
                  'sigma': {'value': self.sigmaValue.value(), 'vary': (not self.sigmaFixedCB.isChecked())},
                  'amplitude': {'value': self.amplitudeValue.value(), 'vary': not self.amplitudeFixedCB.isChecked()}
                  }
                 }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model
