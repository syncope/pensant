# first idea sketch


import fitModels
import pyqtgraph as pg
import numpy as np

class DataPointsWithErorrs():
    def __init__(self, x=None, y=None, yerr=None):
        self._independent = x
        self._dependent = y
        self._error = yerr

    def addData(self, x=None, y=None, yerr=None):
        self._independent = x
        self._dependent = y
        self._error = yerr

    def addIndependentData(self, x=None):
        self._independent = x

    def addDependentData(self, y=None):
        self._dependent = y

    def addErrors(self, yerr=None):
        self._error = yerr

    def basicCheck(self):
        if(len(self._independent) != len(self._dependent)):
            raise RuntimeError("The number of x/y points are different")
        if(len(self._error) != len(self._independent)):
            raise RuntimeError("The number of y points and errors are different")
        else:
            return True

    def get(self):
        return self._independent, self._dependent, self._error


if __name__ == "__main__":
    
    # create some random numbers
    nop = 101
    x = np.linspace(-5.,+5., nop)
    from scipy.stats import norm
    fx = norm(loc = 0., scale = 1.0)
    y = nop*fx.pdf(x)
    yerr = np.sqrt(y)
    
    ymod = y + .2*np.random.normal(loc=y, scale=yerr)
    
    wid = pg.plot(x, ymod)
    ymerr = np.sqrt(ymod)
    err = pg.ErrorBarItem(x=x, y=ymod, height=ymerr )
    wid.addItem(err)

    g = DataPointsWithErorrs(x,ymod, ymerr)
    g.basicCheck()
    
    gauss = fitModels.FitModels["gaussianModel"]
    p0 = {'name':'amplitude', "value": 1. , "variable" : True,  "min" : 0., "max": None}
    p1 ={'name':'center', "value": 2. , "variable" : True,  "min" : None, "max": None}
    p2 = {'name':'sigma', "value": 1.2 , "variable" : True,  "min" : 0., "max": None}
    params = {p['name']: p for p in [p0, p1, p2]}
    gauss.initialize(params)
    fm = gauss.createFitModel()
    print("fitmodel is: " + str(fm))
    k = input()
