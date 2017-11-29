import pyqtgraph as pg
import numpy as np

import fitInterface
import fitfunctions

def main():
    # first create dummy data: gauss with a bit of noise
    # create some testdata, equidistant, 50 points between 0 and 4
    xdata = np.linspace(0, 2, 50)

    # calculate accurate data points according to the function with the given parameters
    y = fitfunctions.gauss()([2.5, .66, 0.5], xdata)

    # now do a simple variation of the accurate data points to leave the fit algorithm with something to do
    ydata = y + 0.2 * np.random.normal(size=len(xdata))
    
    # now define the function to be fitted
    fitfunc = fitfunctions.gauss()
    
    # easiest way to lsfit is to define a residual function
    # !!! NOTE the order of arguments !!!
    def residual(par, xdata, ydata):
        return ydata - fitfunc(par, xdata)
    
    # in principle ready to start -> but still needs a starting point
    startval = [2., 0.5, 0.1]
    
    # so now start the fit:
    fitter = fitInterface.LeastSquaresFitter()
    fitter.fit(residual, startval, arguments=(xdata, ydata))
    fitter.getResult()
    bestvals = fitter.getBestValues()
    
    
    # drawing:
    plotWidget = pg.plot(title="example display")
    plotWidget.plot(xdata, ydata, pen=None, symbol='o')
    plotWidget.plot(xdata, fitfunctions.gauss()(bestvals, xdata))
    
    input("Press Enter to continue...")
   
if __name__=="__main__":
   main()
