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

from fitModels import FitModels



def CurveFitting():
    def  __init__(self, data=None):
        self._data = data
        self._model = None
        self._parameters = None
        pass

    def plot(self):
        '''GUI functionality'''
        pass

    def chooseModel(self, model=''):
        '''Choose a model from the list of available models.'''
        pass

    def getParameters(self):
        '''Returns the list of parameters.'''
        pass

    def setParameter(self, identifier, value):
        pass

    def fit(self):
        '''If data and model defined, perform the fit. Returns result.'''
        pass

    def setupFromJSON(self, jsonobject):
        pass
