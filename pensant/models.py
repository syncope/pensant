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

# extension to lmfit, by subclassing the (most?) relevant models


from lmfit import Model
from lmfit.models import PseudoVoigtModel, LorentzianModel, GaussianModel
from lmfit.models import ConstantModel, LinearModel, QuadraticModel
from lmfit.models import PolynomialModel, ExponentialModel

from PyQt4 import QtCore, QtGui, uic
import numpy as np
import math

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


class GaussianParameterSettingDialog(ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(GaussianParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.meanSlider.valueChanged.connect(self._meanScaler)
        self.amplitudeSlider.valueChanged.connect(self._ampScaler)
        self.sigmaSlider.valueChanged.connect(self._sigmaScaler)
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
        self._meanDisplay = float(np.mean(self._xdata))
        self._meanBounds = (float(np.amin(self._xdata)), float(np.amax(self._xdata)))
        self._sigmaDisplay = float(np.amax(self._xdata) - np.amin(self._xdata))/10.
        self._sigmaBounds = (float(self._sigmaDisplay/10.), float(self._sigmaDisplay*2.))
        self._amplitudeDisplay = float(np.amax(self._ydata))/8.
        self._amplitudeBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))

        # first fix the accuracy of the display
        # number of steps;
        meanStep =(self._meanBounds[1] - self._meanBounds[0])/(self.meanSlider.maximum()-self.meanSlider.minimum())
        meanAcc = math.floor(math.fabs(math.log10(meanStep)))+2
        self.meanValue.setDecimals(meanAcc)
        self.meanLBValue.setDecimals(meanAcc)
        self.meanUBValue.setDecimals(meanAcc)

        amplitudeStep =(self._amplitudeBounds[1] - self._amplitudeBounds[0])/(self.amplitudeSlider.maximum()-self.amplitudeSlider.minimum())
        amplitudeAcc = math.floor(math.fabs(math.log10(amplitudeStep)))+2
        self.amplitudeValue.setDecimals(amplitudeAcc)
        self.amplitudeLBValue.setDecimals(amplitudeAcc)
        self.amplitudeUBValue.setDecimals(amplitudeAcc)

        sigmaStep =(self._sigmaBounds[1] - self._sigmaBounds[0])/(self.sigmaSlider.maximum()-self.sigmaSlider.minimum())
        sigmaAcc = math.floor(math.fabs(math.log10(sigmaStep)))+2
        self.sigmaValue.setDecimals(sigmaAcc)
        self.sigmaLBValue.setDecimals(sigmaAcc)
        self.sigmaUBValue.setDecimals(sigmaAcc)
        

        # now set initial values
        self.meanValue.setValue(self._meanDisplay)
        self.amplitudeValue.setValue(self._amplitudeDisplay)
        self.sigmaValue.setValue(self._sigmaDisplay)

        # and now the boundaries -- as valid for the slider
        # mean:
        self.meanLBValue.setValue(self._meanBounds[0])
        self.meanUBValue.setValue(self._meanBounds[1])
        # amplitude
        self.amplitudeLBValue.setValue(self._amplitudeBounds[0])
        self.amplitudeUBValue.setValue(self._amplitudeBounds[1])
        # sigma
        self.sigmaLBValue.setValue(self._sigmaBounds[0])
        self.sigmaUBValue.setValue(self._sigmaBounds[1])

        self.updateFit.emit()

    def _meanScaler(self, val):
        valuewidth = self._meanBounds[1]-self._meanBounds[0]
        currentVal = (self.meanSlider.minimum() + float(val * self.meanSlider.singleStep()))/(self.meanSlider.maximum() - self.meanSlider.minimum())
        self.meanValue.setValue(self._meanBounds[0] + currentVal*valuewidth)
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
        self._parameters = self._model.make_params(center=self.meanValue.value(), amplitude=self.amplitudeValue.value(), sigma=self.sigmaValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = { self._model.prefix :
                    { 'modeltype': 'gaussianModel',
                     'center': {'value' : self.meanValue.value(), 'vary': ( not self.meanFixedCB.isChecked()) },
                     'sigma' : {'value' : self.sigmaValue.value(), 'vary': (not self.sigmaFixedCB.isChecked()) },
                     'amplitude' : {'value' : self.amplitudeValue.value(), 'vary': not self.amplitudeFixedCB.isChecked() } 
                    }
                }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model

def modelWidgeteer(model, fitModel, uiFilename, xdata, ydata, index):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    formfile = os.path.join(dir_path, uiFilename)
    if model == "gaussianModel":
        return GaussianParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    else:
        return ParameterSettingDialog(uifile=formfile)


class gaussian(GaussianModel):
    def __init__(self, **kwargs):
        super(gaussian, self).__init__(**kwargs)
        self._widget = None

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("gaussianModel", self, "ui/gaussModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        pass # does not work accurately
        #~ return super(gaussian, self).guess(data, **kw)        


class lorentzian(LorentzianModel):
    def __init__(self, **kwargs):
        super(lorentzian, self).__init__(**kwargs)

    def getWidget(self):
        self._widget = modelWidgeteer("ui/lorentzianModelFitParameters.ui")
        return self._widget

    def guess(self, data, **kw):
        return super(lorentzian, self).guess(data, **kw)        


class psv(PseudoVoigtModel):
    def __init__(self, **kwargs):
        super(psv, self).__init__(**kwargs)

    def guess(self, data, **kw):
        return super(psv, self).guess(data, **kw)        


class linear(LinearModel):
    def __init__(self, **kwargs):
        super(linear, self).__init__(**kwargs)

    def getWidget(self):
        self._widget = modelWidgeteer("ui/linearModelFitParameters.ui")
        return self._widget

    def guess(self, data, **kw):
        return super(linear, self).guess(data, **kw)        


class quadratic(QuadraticModel):
    def __init__(self, **kwargs):
        super(quadratic, self).__init__(**kwargs)

    def getWidget(self):
        self._widget = modelWidgeteer("ui/quadraticModelFitParameters.ui")
        return self._widget

    def guess(self, data, **kw):
        return super(quadratic, self).guess(data, **kw)        


class constant(ConstantModel):
    def __init__(self, **kwargs):
        super(constant, self).__init__(**kwargs)    

    def getWidget(self):
        self._widget = modelWidgeteer("ui/constantModelFitParameters.ui")
        return self._widget

    def guess(self, data, **kw):
        return super(constant, self).guess(data, **kw)        



FitModels = { "constantModel" : constant,
              "linearModel" : linear,
              "quadraticModel" : quadratic,
              "gaussianModel" : gaussian,
              "lorentzianModel" : lorentzian,
              #~ "psvModel" : psv,
            }

