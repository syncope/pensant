# Copyright (C) 2018-9  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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

from pensant.plmfit.models import PseudoVoigtModel, LorentzianModel, GaussianModel
from pensant.plmfit.models import ConstantModel, LinearModel, QuadraticModel
from pensant.plmfit.models import ExponentialModel, ExpressionModel
from pensant.plmfit.model import CompositeModel
from pensant.plmfit.parameter import Parameters

import numpy as np

from . import constantParameterSettingWidget
from . import gaussianParameterSettingWidget
from . import linearParameterSettingWidget
from . import lorentzianParameterSettingWidget
from . import parameterSettingWidget
from . import quadraticParameterSettingWidget
from . import shiftedhyperbolaParameterSettingWidget
from . import exponentialParameterSettingWidget

from scipy.interpolate import UnivariateSpline


class peakGuesser():

    def guessMeanFwhmSigmaHeightAmplitude(self, xdata, ydata):
        peaky = np.amax(ydata)
        name = np.where(ydata == peaky)[0][0]
        peakx = xdata[name]
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

    def getWidget(self, xdata=None, ydata=None, name=None):
        self._widget = modelWidgeteer(model="gaussianModel", fitModel=self, uiFilename="ui/gaussModelFitParameters.ui", xdata=xdata, ydata=ydata, name=name)
        return self._widget

    def gaussguess(self, xdata, ydata):
        guesser = peakGuesser()
        guessparams = guesser.guessMeanFwhmSigmaHeightAmplitude(xdata, ydata)
        # parameters need to be created with "make_params", otherwise the covariance will be zero
        return self.make_params(m0_center=guessparams[0],
                                m0_fwhm=guessparams[1],
                                m0_sigma=guessparams[2],
                                m0_height=guessparams[3],
                                m0_amplitude=guessparams[4])


class lorentzian(LorentzianModel):
    def __init__(self, **kwargs):
        super(lorentzian, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, name=None):
        self._widget = modelWidgeteer(model="lorentzianModel", fitModel=self, uiFilename="ui/lorentzianModelFitParameters.ui", xdata=xdata, ydata=ydata, name=name)
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

    def getWidget(self, xdata=None, ydata=None, name=None):
        self._widget = modelWidgeteer(model="linearModel", fitModel=self, uiFilename="ui/linearModelFitParameters.ui", xdata=xdata, ydata=ydata, name=name)
        return self._widget

    def guess(self, data, **kw):
        return super(linear, self).guess(data, **kw)


class quadratic(QuadraticModel):
    def __init__(self, **kwargs):
        super(quadratic, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, name=None):
        self._widget = modelWidgeteer(model="quadraticModel", fitModel=self, uiFilename="ui/quadraticModelFitParameters.ui", xdata=xdata, ydata=ydata, name=name)
        return self._widget

    def guess(self, data, **kw):
        return super(quadratic, self).guess(data, **kw)


class constant(ConstantModel):
    def __init__(self, **kwargs):
        super(constant, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, name=None):
        self._widget = modelWidgeteer(model="constantModel", fitModel=self, uiFilename="ui/constantModelFitParameters.ui", xdata=xdata, ydata=ydata, name=name)
        return self._widget

    def guess(self, data, **kw):
        return super(constant, self).guess(data, **kw)


class exponential(ExponentialModel):
    def __init__(self, **kwargs):
        super(exponential, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, name=None):
        self._widget = modelWidgeteer(model="exponentialModel", fitModel=self, uiFilename="ui/exponentialModelFitParameters.ui", xdata=xdata, ydata=ydata, name=name)
        return self._widget

    def guess(self, data, **kw):
        return super(exponential, self).guess(data, **kw)


class shiftedhyperbola(ExpressionModel):
    def __init__(self, **kwargs):
        super(shiftedhyperbola, self).__init__('a/(x-xzero)', independent_vars=['x'], **kwargs)

    def getWidget(self, xdata=None, ydata=None, name=None):
        self._widget = modelWidgeteer(model="shiftedhyperbolaModel", fitModel=self, uiFilename="ui/shiftedhyperbolaModelFitParameters.ui", xdata=xdata, ydata=ydata, name=name)
        return self._widget

    def guess(self, data, **kw):
        params = Parameters()
        params.add_many(('a', 1), ('xzero', 1))
        return params


FitModels = {"constantModel": constant,
             "linearModel": linear,
             "quadraticModel": quadratic,
             "gaussianModel": gaussian,
             "lorentzianModel": lorentzian,
             "exponentialModel": exponential,
             "shiftedhyperbolaModel": shiftedhyperbola,
             }


def modelWidgeteer(model, fitModel, uiFilename, xdata, ydata, name):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    formfile = os.path.join(dir_path, uiFilename)
    if model == "gaussianModel":
        return gaussianParameterSettingWidget.GaussianParameterSettingWidget(fitModel, xdata, ydata, name=name, uifile=formfile)
    elif model == "lorentzianModel":
        return lorentzianParameterSettingWidget.LorentzianParameterSettingWidget(fitModel, xdata, ydata, name=name, uifile=formfile)
    elif model == "constantModel":
        return constantParameterSettingWidget.ConstantParameterSettingWidget(fitModel, xdata, ydata, name=name, uifile=formfile)
    elif model == "linearModel":
        return linearParameterSettingWidget.LinearParameterSettingWidget(fitModel, xdata, ydata, name=name, uifile=formfile)
    elif model == "quadraticModel":
        return quadraticParameterSettingWidget.QuadraticParameterSettingWidget(fitModel, xdata, ydata, name=name, uifile=formfile)
    elif model == "exponentialModel":
        return exponentialParameterSettingWidget.exponentialParameterSettingWidget(fitModel, xdata, ydata, name=name, uifile=formfile)
    elif model == "shiftedhyperbolaModel":
        return shiftedhyperbolaParameterSettingWidget.shiftedhyperbolaParameterSettingWidget(fitModel, xdata, ydata, name=name, uifile=formfile)
    else:
        return parameterSettingWidget.ParameterSettingWidget(uifile=formfile)
