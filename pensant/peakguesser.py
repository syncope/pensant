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
from scipy.interpolate import UnivariateSpline


class peakGuesser():
    def __init__(self):
        pass

    def guessMeanFwhmAmplitude(self, xdata, ydata):
        peaky = np.amax(ydata)
        index = np.where(ydata == peaky)[0][0]
        peakx = xdata[index]
        halfpeaky = peaky/2.
        f = UnivariateSpline(xdata, ydata-peaky/2., k=3)
        w1, w2 = f.roots()
        fwhm = w2 - w1
        return peakx, fwhm, peaky

    def guessMeanSigmaAmplitude(self, xdata, ydata):
        mean, fwhm, amp = self.guessMeanFwhmAmplitude(xdata, ydata)
        return mean, fwhm/2.3548, amp

#~ if __name__ == "__main__":
    #~ pg = peakGuesser()
    #~ def gaussian(x, mu=5, sig=1.2, a=1):
        #~ return a/(math.sqrt(2*3.1415)*sig)*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
#~
#~
    #~ for n in range(100000):
        #~ x = np.arange(0, 10)
        #~ y = gaussian(x)
        #~ m,f,a = pg.guessMeanFwhmAmplitude(x,y)
        #~ print("result: mu=" + str(m) + " fwhm=" + f + " amp=" + str(a))
        #~ import pyqtgraph as pq
        #~ w = pq.plot(x,y, pen=None, symbolPen='w', symbolBrush='w', symbol='+')
        #~ w.plot(x, gaussian(x, mu=m, sig=f/2.354, a=a*math.sqrt(2*3.1415)*f/2.354))
