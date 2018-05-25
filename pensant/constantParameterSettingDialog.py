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

import parameterSettingDialog

class ConstantParameterSettingDialog(parameterSettingDialog.ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(ConstantParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)

        self.constSlider.valueChanged.connect(self._constScaler)
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
        self._constDisplay = float(np.mean(self._ydata))
        self._constBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))

        # first fix the accuracy of the display
        # number of steps;
        constStep =(self._constBounds[1] - self._constBounds[0])/(self.constSlider.maximum()-self.constSlider.minimum())
        constAcc = math.floor(math.fabs(math.log10(constStep)))+2
        self.constValue.setDecimals(constAcc)
        self.constLBValue.setDecimals(constAcc)
        self.constUBValue.setDecimals(constAcc)

        # now set initial value
        self.constValue.setValue(self._constDisplay)

        # and now the boundaries -- as valid for the slider
        self.constLBValue.setValue(self._constBounds[0])
        self.constUBValue.setValue(self._constBounds[1])

        self.updateFit.emit()

    def _constScaler(self, val):
        valuewidth = self._constBounds[1]-self._constBounds[0]
        currentVal = (self.constSlider.minimum() + float(val * self.constSlider.singleStep()))/(self.constSlider.maximum() - self.constSlider.minimum())
        self.constValue.setValue(self._constBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(c=self.constValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = { self._model.prefix :
                    { 'modeltype': 'constantModel',
                     'c': {'value' : self.constValue.value(), 'vary': ( not self.constFixedCB.isChecked()) },
                    }
                }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model

