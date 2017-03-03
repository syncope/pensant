# define the actual fitfunctions

import numpy as np
import math

import function1d

class gauss(function1d.fitFunction1D):
    def __init__(self):
        super(gauss, self).__init__(3)
        self._fpo.createParameters(["N", "mean", "variance"])

    def _implementation(self, par, x):
        self._fpo.passValueList(par)
        N = self._fpo.getParameterValue("N")
        mean = self._fpo.getParameterValue("mean")
        sigma = math.sqrt(self._fpo.getParameterValue("variance"))
        
        return N* np.exp( - ((x - mean)/sigma)**2 )


class lorentz(function1d.fitFunction1D):
    def __init__(self):
        super(lorentz, self). __init__(3)
        self._fpo.createParameters(["amplitude","position","fwhm"])

    def _implementation(self, par, x):
        self._fpo.passValueList(par)
        amplitude = self._fpo.getParameterValue("amplitude")
        position = self._fpo.getParameterValue("position")
        fwhm = self._fpo.getParameterValue("fwhm")
        
        return amplitude / (1. + np.power((x - position) / (fwhm * 0.5), 2))
#~ 
#~ 
#~ class pseudoVoigt(function1d.fitFunction1D):
    #~ def __init__(self):
        #~ super(pseudeVoigt, self). __init__(ASD)
#~ 
#~ 
    #~ def _implementation(self, par, x):
        #~ return 1.
#~ 


if __name__ == "__main__":
    g1 = gauss()
    g2 = gauss()
    l = lorentz()
    g3 = gauss()
    model = function1d.combined1Dfunction(g1)
    model.addFunction(g2)
    print("values at 0: " + str(g1([1.,0.,3.],0.)) + " and " + str(g2([2.,1.,1.],0.)) + " and " + str(g3( [2.,1.,1.], 0.)))
    print(" lorentzia, liebe lorentzia mein: " + str(l([1.2,3.4,5.6],7.)))
    l.fixParameter("amplitude", 1.2)
    print(" ach wenn doch immer nur sonntag waer: " + str(l([3.4,5.6],7.)))
    
    model([1.,0.,3.,2.,1.,1.], 0.)
    model.multiplyFunction(g3)
    model([1.,0.,3.,2.,1.,1., 2.,1.,1.], 0.)
#~ 
    #~ def resi(p, m, v):
        #~ return model(p, m) - v
#~ 
    #~ bigbadmotorfinger = function1d.fitter()
    #~ bigbadmotorfinger.fit(resi, [1.,0.,3.,2.,1.,1., 2.,1.,1.], (0., 1.3))
