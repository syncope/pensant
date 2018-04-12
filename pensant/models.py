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
    
    def __init__(self, xdata, ydata, **kw):
        super(GaussianParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)

    def update(self):
        self._meanDisplay = ( float(np.mean(self._xdata)), float(np.amin(self._xdata)), float(np.amax(self._xdata)))
        self._amplitudeDisplay =  ( float(np.mean(self._ydata)), float(np.amin(self._ydata)), float(np.amax(self._ydata))) 
        self._sigmaDisplay = (float(self._meanDisplay[2] - self._meanDisplay[1])/3.5)
        self.meanValue.setValue(self._meanDisplay[0])
        self.meanLBValue.setValue(self._meanDisplay[1])
        self.meanUBValue.setValue(self._meanDisplay[2])

        self.amplitudeValue.setValue(self._amplitudeDisplay[0])
        self.amplitudeLBValue.setValue(self._amplitudeDisplay[1])
        self.amplitudeUBValue.setValue(self._amplitudeDisplay[2])

        self.sigmaValue.setValue(self._sigmaDisplay)

def modelWidgeteer(model, uiFilename, xdata, ydata):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    formfile = os.path.join(dir_path, uiFilename)
    if model == "gaussian":
        return GaussianParameterSettingDialog(xdata, ydata, uifile=formfile)

class gaussian(GaussianModel):
    def __init__(self, **kwargs):
        super(gaussian, self).__init__(**kwargs)
        self._widget = None

    def getWidget(self, xdata=None, ydata=None):
        self._widget = modelWidgeteer("gaussian", "ui/gaussModelFitParameters.ui", xdata, ydata)
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
