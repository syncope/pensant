
# the master class to steer the complete fitting procedure:
# - define the function to fit in terms of residual
# 

from scipy.optimize import leastsq
import numpy as np

import function1d
import fitfunctions


class fitResult():
    def __init__(self):
        pass

    def success(self):
        pass




class fitInterface():
    
    def __init__(self):
        pass
    
    def fit(self):
        pass

    def getResult(self):
        pass

class LeastSquaresFitter(fitInterface):
    
    def __init__(self):
        self._result = None

    def fit(self, residual, startvalues, arguments=None):
        self._result = leastsq(residual, startvalues, args=arguments, full_output=True)

    def getResult(self):
        if self._result == None:
            raise RuntimeError("Can't fetch result. Has the fit run?")
        print("+"*80 + "\n"  + "+"*80)
        print("status integer is [" + str(self._result[4]) + "] meaning:\n    " + str(self._result[3]))
        print("routine was called [" + str(self._result[2]["nfev"]) + "] times.")
        print("best values: " + str(self._result[0]))
        print("covariance matrix: \n " + str(self._result[1]))
        print("+"*80 + "\n"  + "+"*80)

    def getBestValues(self):
        if self._result == None:
            raise RuntimeError("Can't fetch result. Has the fit run?") 
        return self._result[0]
