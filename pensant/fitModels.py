# Copyright (C) 2017  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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

# model definitions, just take what's predefined in lmfit

from lmfit import  Model
from lmfit.models import PseudoVoigtModel, LorentzianModel, GaussianModel
from lmfit.models import ConstantModel, LinearModel, QuadraticModel
from lmfit.models import PolynomialModel, ExponentialModel


class fitParameter():
    '''Abstract definition of a fit parameter interface.'''

    def __init__(self, obj):
        try:
            self._name = obj["name"]
            self._value = obj["value"]
            self._variable = obj["variable"]
            self._min = obj["min"]
            self._max = obj["max"]
        except KeyError("[fitParameter] The parameter is not fully qualified, at least one element is missing."):
            exit()

    def name(self):
        return self._name
    
    def value(self):
        return self._value

    def variable(self):
        return self._variable

    def min(self):
        return self._min

    def max(self):
        return self._max


class iModelDescription():

    def __init__(self):
        self._model = None
        self._prefix = None
        self._name = None
        self._nop = None
        self._paramnames = ()
        self._parameters = {}

    def initialize(self, configDict):
        '''Create the map of parameters from a dictionary.
           First checks for number of elements, then uses the given dictionary to create actual parameter objects.'''
        
        if len(configDict) != self._nop:
            raise TypeError("[ModelDescription]: The chosen model has a different number of parameters than supplied.")

        try:
            for name in self._paramnames:
                self._parameters[name] = fitParameter(configDict[name])
        except KeyError("[ModelDescription:initialize] The given dict is not compatible with the chosen type of model/parameter."):
            exit()
        
    def createFitModel(self):
        modelparameters = self._model.make_params()
        for name, fitparam in self._parameters.items():
            modelparameters[name].set(value=fitparam.value(), vary=fitparam.variable(), min=fitparam.min(), max=fitparam.max())

class constant(iModelDescription):

    def __init__(self):
        super(constant, self).__init__()
        self._model = ConstantModel()
        self._nop = 1
        self._paramnames = ('c')


class linear(iModelDescription):

    def __init__(self):
        super(linear, self).__init__()
        self._model = LinearModel()
        self._nop = 2
        self._paramnames = ('intercept', 'slope')

class quadratic(iModelDescription):

    def __init__(self):
        super(quadratic, self).__init__()
        self._model = QuadraticModel()
        self._nop = 3
        self._paramnames = ('a', 'b', 'c')

class gaussian(iModelDescription):

    def __init__(self):
        super(gaussian, self).__init__()
        self._model = GaussianModel()
        self._nop = 3
        self._paramnames = ('sigma', 'center', 'amplitude')

class lorentzian(iModelDescription):

    def __init__(self):
        super(lorentzian, self).__init__()
        self._model = LorentzianModel()
        self._nop = 3
        self._paramnames = ('sigma', 'center', 'amplitude')

class psv(iModelDescription):

    def __init__(self):
        super(psv, self).__init__()
        self._model = PseudoVoigtModel()
        self._nop = 4
        self._paramnames = ('sigma', 'center', 'fraction', 'amplitude')


FitModels = { "constantModel" : constant(),
              "linearModel" : linear(),
              "quadraticModel" : quadratic(),
              "gaussianModel" : gaussian(),
              "lorentzianModel" : lorentzian(),
              "psvModel" : psv(),
            }

if __name__ == "__main__":
    cm = constant()
    param = {"name": "somtest", "value": 2.345 , "variable" : False, "min" : -1., "max": +3.45}
    params = { "c": param}
    cm.initialize(params)
    fm = cm.createFitModel()

