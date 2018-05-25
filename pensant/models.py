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

import constantParameterSettingDialog
import gaussianParameterSettingDialog
import linearParameterSettingDialog
import lorentzianParameterSettingDialog
import parameterSettingDialog
import quadraticParameterSettingDialog.py


class gaussian(GaussianModel):
    def __init__(self, **kwargs):
        super(gaussian, self).__init__(**kwargs)
        self._widget = None

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("gaussianModel", self, "ui/gaussModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        pass # does not work accurately



class lorentzian(LorentzianModel):
    def __init__(self, **kwargs):
        super(lorentzian, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("lorentzianModel", self, "ui/lorentzianModelFitParameters.ui", xdata, ydata, index)
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

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("linearModel", self, "ui/linearModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        return super(linear, self).guess(data, **kw)        



class quadratic(QuadraticModel):
    def __init__(self, **kwargs):
        super(quadratic, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("quadraticModel", self, "ui/quadraticModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        return super(quadratic, self).guess(data, **kw)        



class constant(ConstantModel):
    def __init__(self, **kwargs):
        super(constant, self).__init__(**kwargs)    

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("constantModel", self, "ui/constantModelFitParameters.ui", xdata, ydata, index)
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



def modelWidgeteer(model, fitModel, uiFilename, xdata, ydata, index):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    formfile = os.path.join(dir_path, uiFilename)
    if model == "gaussianModel":
        return gaussianParameterSettingDialog.GaussianParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "lorentzianModel":
        return lorentzianParameterSettingDialog.LorentzianParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "constantModel":
        return constantParameterSettingDialog.ConstantParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "linearModel":
        return linearParameterSettingDialog.LinearParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "quadraticModel":
        return quadraticParameterSettingDialog.QuadraticParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    else:
        return parameterSettingDialog.ParameterSettingDialog(uifile=formfile)

