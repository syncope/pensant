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

#  the master interface class needed for gui and everything else

import fitModels


class CurveFitting():
    def  __init__(self):
        self._data = None
        self._model = None
        self._parameters = None

    #~ def plot(self):
        #~ '''GUI functionality'''
        #~ pass

    def chooseModel(self, model=None):
        '''Choose a model from the list of available models.'''
        try:
            self._model = fitModels.FitModels[model]
        except KeyError("Chosen model: " + str(model) + " does not exist. Exiting."):
            exit()

    def getParameterNames(self):
        '''Returns the list of parameters.'''
        return self._model.getParameterNames()

    def setParameters(self, configDict):
        '''Accepts a dictionary holding the parameter names and values.'''
        try:
            self._model.initialize(configDict)
        except:
            print("[CurveFitting::setParameters] Exception occured. Exiting.")
            exit()

    def fit(self):
        '''If data and model defined, perform the fit. Returns result.'''
        pass

    def dump(self):
        self._model.dump()
