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

fitModels = { "constantModel" : ConstantModel(),
              "linearModel" : LinearModel(),
              "quadraticModel" : QuadraticModel(),
              "gaussianModel" : GaussianModel(),
              "lorentzianModel" : LorentzianModel(),
              "psvModel" : PseudoVoigtModel(),
            }
