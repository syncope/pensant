# 1d functions

# abstract function definition
# sets the basic structure and how to add/multiply functions


from scipy.optimize import leastsq
import numpy as np


class fitParameter():

    def __init__(self, value=None, name=None, fixed=False, limits=(), dtype='float'):
        self._value = value
        self._name = name
        self._fixed = fixed
        self._limits = limits
        self._dtype = dtype

    def setName(self, name):
        self._name = name

    def setValue(self, value):
        self._value = value

    def setFixed(self):
        self._fixed = True

    def setFree(self):
        self._fixed = False

    def setLimits(self, limits):
        self._limits = limits

    def setDType(self, dtype):
        self._dtype = dtype

    def getName(self):
        return self._name

    def getValue(self):
        return self._value

    def isFixed(self):
        return self._fixed

    def getLimits(self):
        return self._limits

    def getDType(self):
        return self._dtype

    def __call__(self):
        return self._value


class fitParameterObject():
    def __init__(self, n):
        self._maxN = n
        self._map = {}
        self._parOrder = []
        self._nfixed = 0

    def getNumberOfFreeParameters(self):
        return self._maxN - self._nfixed

    def createParameters(self, nameList):
        if len(nameList) != self._maxN:
            raise ValueError("The function has " + self._maxN +
                             " parameters, but " + len(nameList) +
                             " names were given.")
        self._parOrder = nameList
        for name in nameList:
            self._map[name] = fitParameter(name=name)

    def getParameterValue(self, name):
        return self._map[name].getValue()

    def fixParameter(self, name, value):
        self._map[name].setFixed()
        self._map[name].setValue(value)
        self._nfixed += 1

    def freeParameter(self, name):
        if self._map[name].isFixed():
            self._map[name].setFree()
            self._nfixed -= 1

    def passValueList(self, par):
        if len(par) != (self._maxN - self._nfixed):
            raise RuntimeError("The number of values passed to the " +
                               "function doesn't match the number of " +
                               "free parameters.")
        index = 0
        for parname in self._parOrder:
            if self._map[parname].isFixed():
                continue
            else:
                self._map[parname].setValue(par[index])
                index += 1



class fitFunction1D():

    def __init__(self, npar):
        self._fpo = fitParameterObject(npar)

    def getNumberOfParameters(self):
        return self._fpo.getNumberOfFreeParameters()

    def fixParameter(self, name, value):
       self._fpo.fixParameter(name, value)

    def freeParameter(self, name):
        self._fpo.freeParameter(name)

    def __call__(self, par, x):
        try:
            return self._implementation(par, x)
        except IndexError("The number of parameters in the function \
                             doesn't match the given number of \
                             non-fixed parameters."):
            pass

    def _implementation(self, par, x):
        pass


class combined1Dfunction(fitFunction1D):

    def __init__(self, func):
        self._f = [func]
        self._FUNC = "value[0]"
        self._tnop = func.getNumberOfParameters()

    def _updateNumbers(self):
        n = 0
        for f in self._f:
            n += f.getNumberOfParameters()
        self._tnop  = n

    def _implementation(self, par, x):
        value = self._calculateComponents(par, x)
        print(eval(self._FUNC))

    def _calculateComponents(self, par, x):
        paroffset = 0
        results = []
        for f in self._f:
            nop = paroffset + f.getNumberOfParameters()
            results.append( f(par[paroffset:nop],x) )
            paroffset = nop
        return results
        
    def addFunction(self, func):
        self._f.append(func)
        self._updateNumbers()
        self._FUNC = "("  + self._FUNC + " + value[" + str(self._f.index(func)) + "])"

    def multiplyFunction(self, func):
        self._f.append(func)
        self._updateNumbers()
        self._FUNC = "("  + self._FUNC + " * value[" + str(self._f.index(func)) + "])"
