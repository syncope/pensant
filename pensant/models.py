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

class ParameterSettingDialog(QtGui.QDialog):
    updateFit = QtCore.pyqtSignal()

    def __init__(self, uifile, parent=None):
        super(ParameterSettingDialog, self).__init__(parent)
        uic.loadUi(uifile, self)

    def passData(self, xdata, ydata):
        self._xdata = xdata
        self._ydata = ydata
        self.update()

    def update(self):
        pass

class GaussianParameterSettingDialog(ParameterSettingDialog):
    

    def __init__(self, xdata, ydata, model=None, **kw):
        super(GaussianParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.meanSlider.valueChanged.connect(self._meanScaler)
        self.amplitudeSlider.valueChanged.connect(self._ampScaler)
        self.sigmaSlider.valueChanged.connect(self._sigmaScaler)
        self._model = model

    def update(self):
        # first basic calculations 
        self._meanDisplay = float(np.mean(self._xdata))
        self._meanBounds = (float(np.amin(self._xdata)), float(np.amax(self._xdata)))
        self._sigmaDisplay = float(np.amax(self._xdata) - np.amin(self._xdata))/5.
        self._amplitudeDisplay = float(np.amax(self._ydata))/5.
        # now set initial values
        self.meanValue.setValue(self._meanDisplay)
        self.amplitudeValue.setValue(self._amplitudeDisplay)
        self.sigmaValue.setValue(self._sigmaDisplay)

        # and now the boundaries -- as valid for the slider
        # mean:
        self.meanLBValue.setValue(float(np.amin(self._xdata)))
        self.meanUBValue.setValue(float(np.amax(self._xdata)))
        # amplitude
        self.amplitudeLBValue.setValue(float(np.amin(self._ydata)))
        self.amplitudeUBValue.setValue(float(np.amax(self._ydata)))
        # sigma
        self.sigmaLBValue.setValue(self._sigmaDisplay/5.)
        self.sigmaUBValue.setValue(self._sigmaDisplay*5)
        self.updateFit.emit()

    def _meanScaler(self, val):
        valuewidth = self._meanBounds[1]-self._meanBounds[0]
        currentVal = (self.meanSlider.minimum() + val * self.meanSlider.singleStep())/(self.meanSlider.maximum() - self.meanSlider.minimum())
        self.meanValue.setValue(self._meanBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _ampScaler(self, val):
        valuewidth = self.amplitudeUBValue.value() - self.amplitudeLBValue.value()
        currentVal = (self.amplitudeSlider.minimum() + val * self.amplitudeSlider.singleStep())/(self.amplitudeSlider.maximum() - self.amplitudeSlider.minimum())
        self.amplitudeValue.setValue(self.amplitudeLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def _sigmaScaler(self, val):
        valuewidth = self.sigmaUBValue.value() - self.sigmaLBValue.value()
        currentVal = (self.sigmaSlider.minimum() + val * self.sigmaSlider.singleStep())/(self.sigmaSlider.maximum() - self.sigmaSlider.minimum())
        self.sigmaValue.setValue(self.sigmaLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        params = self._model.make_params(center=self.meanValue.value(), amplitude=self.amplitudeValue.value(), sigma=self.sigmaValue.value())
        return self._model.eval(params, x=self._xdata) 

def modelWidgeteer(model, fitModel, uiFilename, xdata, ydata):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    formfile = os.path.join(dir_path, uiFilename)
    if model == "gaussian":
        return GaussianParameterSettingDialog(xdata, ydata, fitModel, uifile=formfile)
    else:
        return ParameterSettingDialog(uifile=formfile)

class gaussian(GaussianModel):
    def __init__(self, **kwargs):
        super(gaussian, self).__init__(**kwargs)
        self._widget = None

    def getWidget(self, xdata=None, ydata=None):
        self._widget = modelWidgeteer("gaussian", self, "ui/gaussModelFitParameters.ui", xdata, ydata)
        return self._widget

    def guess(self, data, **kw):
        retval = super(gaussian, self).guess(data, **kw)        

class lorentzian(LorentzianModel):
    def __init__(self, **kwargs):
        super(lorentzian, self).__init__(**kwargs)

    def getWidget(self):
        self._widget = modelWidgeteer("ui/lorentzianModelFitParameters.ui")
        return self._widget


class psv(PseudoVoigtModel):
    def __init__(self, **kwargs):
        super(psv, self).__init__(**kwargs)

class linear(LinearModel):
    def __init__(self, **kwargs):
        super(linear, self).__init__(**kwargs)

    def getWidget(self):
        self._widget = modelWidgeteer("ui/linearModelFitParameters.ui")
        return self._widget

class quadratic(QuadraticModel):
    def __init__(self, **kwargs):
        super(quadratic, self).__init__(**kwargs)

    def getWidget(self):
        self._widget = modelWidgeteer("ui/quadraticModelFitParameters.ui")
        return self._widget

class constant(ConstantModel):
    def __init__(self, **kwargs):
        super(constant, self).__init__(**kwargs)    

    def getWidget(self):
        self._widget = modelWidgeteer("ui/constantModelFitParameters.ui")
        return self._widget

FitModels = { "constantModel" : constant,
              "linearModel" : linear,
              "quadraticModel" : quadratic,
              "gaussianModel" : gaussian,
              "lorentzianModel" : lorentzian,
              #~ "psvModel" : psv,
            }
