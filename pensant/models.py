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

from pensant.plmfit import Model
from pensant.plmfit.models import PseudoVoigtModel, LorentzianModel, GaussianModel
from pensant.plmfit.models import ConstantModel, LinearModel, QuadraticModel
from pensant.plmfit.models import PolynomialModel, ExponentialModel
from pensant.plmfit.models import ExpressionModel
from pensant.plmfit.parameter import Parameters

from PyQt4 import QtCore, QtGui, uic
import numpy as np
import math

from . import constantParameterSettingDialog
from . import gaussianParameterSettingDialog
from . import linearParameterSettingDialog
from . import lorentzianParameterSettingDialog
from . import parameterSettingDialog
from . import quadraticParameterSettingDialog
from . import shiftedhyperbolaParameterSettingDialog
#~ from . import exponentialParameterSettingDialog

from scipy.interpolate import UnivariateSpline

class peakGuesser():

    def guessMeanFwhmSigmaHeightAmplitude(self, xdata, ydata):
        peaky = np.amax(ydata)
        index = np.where(ydata == peaky)[0][0]
        peakx = xdata[index]
        halfpeaky = peaky/2.
        f = UnivariateSpline(xdata, ydata-peaky/2., k=3)
        try:
            w1, w2 = f.roots()
            fwhm = w2 - w1
        except:
            fwhm = (np.amax(xdata) - np.amin(xdata))/2.
        return peakx, fwhm, fwhm/2.3548, peaky, peaky


class gaussian(GaussianModel):
    def __init__(self, **kwargs):
        super(gaussian, self).__init__(**kwargs)
        self._widget = None

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("gaussianModel", self, "ui/gaussModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def gaussguess(self, xdata, ydata):
        guesser = peakGuesser()
        params = Parameters()
        guessparams = guesser.guessMeanFwhmSigmaHeightAmplitude(xdata, ydata)
        params.add_many(('m0_center', guessparams[0]),
                        ('m0_fwhm', guessparams[1]),
                        ('m0_sigma', guessparams[2]),
                        ('m0_height', guessparams[3]),
                        ('m0_amplitude', guessparams[4]))
        return params


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


class exponential(ExponentialModel):
    def __init__(self, **kwargs):
        super(exponential, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("exponentialModel", self, "ui/exponentialModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        return super(exponential, self).guess(data, **kw)


class shiftedhyperbola(ExpressionModel):
    def __init__(self, **kwargs):
        super(shiftedhyperbola, self).__init__('a/(x-xzero)', independent_vars=['x'], **kwargs)

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("shiftedhyperbolaModel", self, "ui/shiftedhyperbolaModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        params = Parameters()
        params.add_many(('a', 1), ('xzero', 1))
        return params

#~ class shiftedexponential(ExpressionModel):
    #~ def __init__(self, **kwargs):
        #~ super(shiftedexponential, self).__init__(**kwargs)
        #~ self = ExpressionModel('amp*exp(-lambda*(x-x0))-offset')

    #~ def getWidget(self, xdata=None, ydata=None, index=None):
        #~ self._widget = modelWidgeteer("exponentialModel", self, "ui/exponentialModelFitParameters.ui", xdata, ydata, index)
        #~ return self._widget


FitModels = {"constantModel": constant,
             "linearModel": linear,
             #~ "quadraticModel": quadratic,
             "gaussianModel": gaussian,
             "lorentzianModel": lorentzian,
             #~ "exponentialModel": exponential,
             "shiftedhyperbolaModel": shiftedhyperbola,
             #~ "shiftedexponentialModel": exponential,
             # "psvModel" : psv,
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
    elif model == "exponentialModel":
        return exponentialParameterSettingDialog.exponentialParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    #~ elif model == "shiftedexponentialModel":
        #~ return shiftedexponentialParameterSettingDialog.shiftedexponentialParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "shiftedhyperbolaModel":
        return shiftedhyperbolaParameterSettingDialog.shiftedhyperbolaParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    else:
        return parameterSettingDialog.ParameterSettingDialog(uifile=formfile)
