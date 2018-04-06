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

# a simple guessing mechanism to extract parameters from 1D data

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline


class peakGuesser():
    def __init__(self):
        pass

    def guess(self, xdata, ydata):
        peaky = np.amax(ydata)
        peakx = xdata[np.where(ydata==peaky)]
        halfpeaky = peaky/2.
        f = InterpolatedUnivariateSpline(xdata, ydata)
        derivative = f.derivative()
        derivative.roots()
        return f

if __name__ == "__main__":
    pg = peakGuesser()
    x = np.arange(0, 10)
    def gaussian(x, mu=3, sig=1.):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    y = gaussian(x)
    k = pg.guess(x,y)
    import pyqtgraph as pq
    #~ w = pq.plot(x,k(y))
    w = pq.plot(x,y, pen=None, symbolPen='w', symbolBrush='w', symbol='+')
    w.plot(x,k(x))
    s = input("type something")
