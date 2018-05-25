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

# extension to lmfit, by subclassing the (most?) relevant models


from lmfit import Model
from lmfit.models import PseudoVoigtModel, LorentzianModel, GaussianModel
from lmfit.models import ConstantModel, LinearModel, QuadraticModel
from lmfit.models import PolynomialModel, ExponentialModel

from PyQt4 import QtCore, QtGui, uic
import numpy as np
import math

class ParameterSettingDialog(QtGui.QDialog):
    updateFit = QtCore.pyqtSignal()
    guessingDone = QtCore.pyqtSignal()

    def __init__(self, uifile, index=None, parent=None):
        super(ParameterSettingDialog, self).__init__(parent)
        uic.loadUi(uifile, self)
        self._index = index

    def passData(self, xdata, ydata):
        self._xdata = xdata
        self._ydata = ydata
        self.update()

    def update(self):
        pass

    def getIndex(self):
        return self._index


class GaussianParameterSettingDialog(ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(GaussianParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        #~ self.meanValue.editingFinished.connect(self._updateMeanSlider)
        #~ self.amplitudeValue.editingFinished.connect(self._updateAmplitudeSlider)
        #~ self.sigmaValue.editingFinished.connect(self._updateSigmaSlider)
        self.meanSlider.valueChanged.connect(self._meanScaler)
        self.amplitudeSlider.valueChanged.connect(self._ampScaler)
        self.sigmaSlider.valueChanged.connect(self._sigmaScaler)
        self._modelName = modelname
        self._model = model
        self._model.prefix = "m" + str(self._index) + "_"
        self._parameters = None
        self.guessStartValuesBtn.clicked.connect(print)
        self.configDonePushBtn.clicked.connect(self._guessingDone)

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def _updateSigmaSlider(self,value):
        pass

    def _updateAmplitudeSlider(self,value):
        pass

    def _updateMeanSlider(self,value):
        pass


    def update(self):
        # first basic calculations 
        self._meanDisplay = float(np.mean(self._xdata))
        self._meanBounds = (float(np.amin(self._xdata)), float(np.amax(self._xdata)))
        self._sigmaDisplay = float(np.amax(self._xdata) - np.amin(self._xdata))/10.
        self._sigmaBounds = (float(self._sigmaDisplay/10.), float(self._sigmaDisplay*2.))
        self._amplitudeDisplay = float(np.amax(self._ydata))/10.
        lowerAmpBound = float(np.amin(self._ydata))
        if lowerAmpBound < 0.:
            lowerAmpBound = 0.
        self._amplitudeBounds = (lowerAmpBound, float(np.amax(self._ydata))/(10*self._sigmaBounds[1]))

        # first fix the accuracy of the display
        # number of steps;
        meanStep =(self._meanBounds[1] - self._meanBounds[0])/(self.meanSlider.maximum()-self.meanSlider.minimum())
        meanAcc = math.floor(math.fabs(math.log10(meanStep)))+2
        self.meanValue.setDecimals(meanAcc)
        self.meanLBValue.setDecimals(meanAcc)
        self.meanUBValue.setDecimals(meanAcc)

        amplitudeStep =(self._amplitudeBounds[1] - self._amplitudeBounds[0])/(self.amplitudeSlider.maximum()-self.amplitudeSlider.minimum())
        amplitudeAcc = math.floor(math.fabs(math.log10(amplitudeStep)))+2
        self.amplitudeValue.setDecimals(amplitudeAcc)
        self.amplitudeLBValue.setDecimals(amplitudeAcc)
        self.amplitudeUBValue.setDecimals(amplitudeAcc)

        sigmaStep =(self._sigmaBounds[1] - self._sigmaBounds[0])/(self.sigmaSlider.maximum()-self.sigmaSlider.minimum())
        sigmaAcc = math.floor(math.fabs(math.log10(sigmaStep)))+2
        self.sigmaValue.setDecimals(sigmaAcc)
        self.sigmaLBValue.setDecimals(sigmaAcc)
        self.sigmaUBValue.setDecimals(sigmaAcc)

        # now set initial values
        self.meanValue.setValue(self._meanDisplay)
        self.amplitudeValue.setValue(self._amplitudeDisplay)
        self.sigmaValue.setValue(self._sigmaDisplay)

        # and now the boundaries -- as valid for the slider
        # mean:
        self.meanLBValue.setValue(self._meanBounds[0])
        self.meanUBValue.setValue(self._meanBounds[1])
        # amplitude
        self.amplitudeLBValue.setValue(self._amplitudeBounds[0])
        self.amplitudeUBValue.setValue(self._amplitudeBounds[1])
        # sigma
        self.sigmaLBValue.setValue(self._sigmaBounds[0])
        self.sigmaUBValue.setValue(self._sigmaBounds[1])

        self.updateFit.emit()

    def _meanScaler(self, val):
        valuewidth = self._meanBounds[1]-self._meanBounds[0]
        currentVal = (self.meanSlider.minimum() + float(val * self.meanSlider.singleStep()))/(self.meanSlider.maximum() - self.meanSlider.minimum())
        self.meanValue.setValue(self._meanBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _ampScaler(self, val):
        valuewidth = self.amplitudeUBValue.value() - self.amplitudeLBValue.value()
        currentVal = (self.amplitudeSlider.minimum() + val * self.amplitudeSlider.singleStep())/(self.amplitudeSlider.maximum() - self.amplitudeSlider.minimum())
        self.amplitudeValue.setValue(self.amplitudeLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def _sigmaScaler(self, val):
        valuewidth = self.sigmaUBValue.value() - self.sigmaLBValue.value()
        currentVal = (self.sigmaSlider.minimum() + float(val * self.sigmaSlider.singleStep()))/(self.sigmaSlider.maximum() - self.sigmaSlider.minimum())
        self.sigmaValue.setValue(self.sigmaLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(center=self.meanValue.value(), amplitude=self.amplitudeValue.value(), sigma=self.sigmaValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = { self._model.prefix :
                    { 'modeltype': 'gaussianModel',
                     'center': {'value' : self.meanValue.value(), 'vary': ( not self.meanFixedCB.isChecked()) },
                     'sigma' : {'value' : self.sigmaValue.value(), 'vary': (not self.sigmaFixedCB.isChecked()) },
                     'amplitude' : {'value' : self.amplitudeValue.value(), 'vary': not self.amplitudeFixedCB.isChecked() } 
                    }
                }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model

def modelWidgeteer(model, fitModel, uiFilename, xdata, ydata, index):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    formfile = os.path.join(dir_path, uiFilename)
    if model == "gaussianModel":
        return GaussianParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "lorentzianModel":
        return LorentzianParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "constantModel":
        return ConstantParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "linearModel":
        return LinearParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    elif model == "quadraticModel":
        return QuadraticParameterSettingDialog(model, xdata, ydata, fitModel, index=index, uifile=formfile)
    else:
        return ParameterSettingDialog(uifile=formfile)


class gaussian(GaussianModel):
    def __init__(self, **kwargs):
        super(gaussian, self).__init__(**kwargs)
        self._widget = None

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("gaussianModel", self, "ui/gaussModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        pass # does not work accurately
        #~ return super(gaussian, self).guess(data, **kw)        


class lorentzian(LorentzianModel):
    def __init__(self, **kwargs):
        super(lorentzian, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("lorentzianModel", self, "ui/lorentzianModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        return super(lorentzian, self).guess(data, **kw)        



class LorentzianParameterSettingDialog(ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(LorentzianParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.centerSlider.valueChanged.connect(self._centerScaler)
        self.amplitudeSlider.valueChanged.connect(self._ampScaler)
        self.sigmaSlider.valueChanged.connect(self._sigmaScaler)
        self._modelName = modelname
        self._model = model
        self._model.prefix = "m" + str(self._index) + "_"
        self._parameters = None
        self.guessStartValuesBtn.clicked.connect(print)
        self.configDonePushBtn.clicked.connect(self._guessingDone)

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # first basic calculations 
        self._centerDisplay = float(np.mean(self._xdata))
        self._centerBounds = (float(np.amin(self._xdata)), float(np.amax(self._xdata)))
        self._sigmaDisplay = float(np.amax(self._xdata) - np.amin(self._xdata))/10.
        self._sigmaBounds = (float(self._sigmaDisplay/10.), float(self._sigmaDisplay*2.))
        self._amplitudeDisplay = float(np.amax(self._ydata))/8.
        self._amplitudeBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))

        # first fix the accuracy of the display
        # number of steps;
        centerStep =(self._centerBounds[1] - self._centerBounds[0])/(self.centerSlider.maximum()-self.centerSlider.minimum())
        centerAcc = math.floor(math.fabs(math.log10(centerStep)))+2
        self.centerValue.setDecimals(centerAcc)
        self.centerLBValue.setDecimals(centerAcc)
        self.centerUBValue.setDecimals(centerAcc)

        amplitudeStep =(self._amplitudeBounds[1] - self._amplitudeBounds[0])/(self.amplitudeSlider.maximum()-self.amplitudeSlider.minimum())
        amplitudeAcc = math.floor(math.fabs(math.log10(amplitudeStep)))+2
        self.amplitudeValue.setDecimals(amplitudeAcc)
        self.amplitudeLBValue.setDecimals(amplitudeAcc)
        self.amplitudeUBValue.setDecimals(amplitudeAcc)

        sigmaStep =(self._sigmaBounds[1] - self._sigmaBounds[0])/(self.sigmaSlider.maximum()-self.sigmaSlider.minimum())
        sigmaAcc = math.floor(math.fabs(math.log10(sigmaStep)))+2
        self.sigmaValue.setDecimals(sigmaAcc)
        self.sigmaLBValue.setDecimals(sigmaAcc)
        self.sigmaUBValue.setDecimals(sigmaAcc)
        

        # now set initial values
        self.centerValue.setValue(self._centerDisplay)
        self.amplitudeValue.setValue(self._amplitudeDisplay)
        self.sigmaValue.setValue(self._sigmaDisplay)

        # and now the boundaries -- as valid for the slider
        # center:
        self.centerLBValue.setValue(self._centerBounds[0])
        self.centerUBValue.setValue(self._centerBounds[1])
        # amplitude
        self.amplitudeLBValue.setValue(self._amplitudeBounds[0])
        self.amplitudeUBValue.setValue(self._amplitudeBounds[1])
        # sigma
        self.sigmaLBValue.setValue(self._sigmaBounds[0])
        self.sigmaUBValue.setValue(self._sigmaBounds[1])

        self.updateFit.emit()

    def _centerScaler(self, val):
        valuewidth = self._centerBounds[1]-self._centerBounds[0]
        currentVal = (self.centerSlider.minimum() + float(val * self.centerSlider.singleStep()))/(self.centerSlider.maximum() - self.centerSlider.minimum())
        self.centerValue.setValue(self._centerBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _ampScaler(self, val):
        valuewidth = self.amplitudeUBValue.value() - self.amplitudeLBValue.value()
        currentVal = (self.amplitudeSlider.minimum() + val * self.amplitudeSlider.singleStep())/(self.amplitudeSlider.maximum() - self.amplitudeSlider.minimum())
        self.amplitudeValue.setValue(self.amplitudeLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def _sigmaScaler(self, val):
        valuewidth = self.sigmaUBValue.value() - self.sigmaLBValue.value()
        currentVal = (self.sigmaSlider.minimum() + float(val * self.sigmaSlider.singleStep()))/(self.sigmaSlider.maximum() - self.sigmaSlider.minimum())
        self.sigmaValue.setValue(self.sigmaLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(center=self.centerValue.value(), amplitude=self.amplitudeValue.value(), sigma=self.sigmaValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = { self._model.prefix :
                    { 'modeltype': 'lorentzianModel',
                     'center': {'value' : self.centerValue.value(), 'vary': ( not self.centerFixedCB.isChecked()) },
                     'sigma' : {'value' : self.sigmaValue.value(), 'vary': (not self.sigmaFixedCB.isChecked()) },
                     'amplitude' : {'value' : self.amplitudeValue.value(), 'vary': not self.amplitudeFixedCB.isChecked() } 
                    }
                }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model
#~ 

class psv(PseudoVoigtModel):
    def __init__(self, **kwargs):
        super(psv, self).__init__(**kwargs)

    def guess(self, data, **kw):
        return super(psv, self).guess(data, **kw)        


class linear(LinearModel):
    def __init__(self, **kwargs):
        super(linear, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("linearModel", self, "ui/linearModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        return super(linear, self).guess(data, **kw)        


class LinearParameterSettingDialog(ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(LinearParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.interceptSlider.valueChanged.connect(self._interceptScaler)
        self.slopeSlider.valueChanged.connect(self._slopeScaler)
        self._modelName = modelname
        self._model = model
        self._model.prefix = "m" + str(self._index) + "_"
        self._parameters = None
        self.guessStartValuesBtn.clicked.connect(print)
        self.configDonePushBtn.clicked.connect(self._guessingDone)

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # first basic calculations 
        self._slopeDisplay = float(np.mean(self._ydata))/float(np.mean(self._xdata))
        self._slopeBounds = (10*self._slopeDisplay, -10*self._slopeDisplay)
        self._interceptDisplay = 0.
        self._interceptBounds = (-1*float(np.amax(self._ydata)), float(np.amax(self._ydata)))

        # first fix the accuracy of the display
        # number of steps;
        #~ slopeStep =(self._slopeBounds[1] - self._slopeBounds[0])/(self.slopeSlider.maximum()-self.slopeSlider.minimum())
        #~ slopeAcc = math.floor(math.fabs(math.log10(slopeStep)))+2
        #~ self.slopeValue.setDecimals(slopeAcc)
        #~ self.slopeLBValue.setDecimals(slopeAcc)
        #~ self.slopeUBValue.setDecimals(slopeAcc)
#~ 
        #~ interceptStep =(self._interceptBounds[1] - self._interceptBounds[0])/(self.interceptSlider.maximum()-self.interceptSlider.minimum())
        #~ interceptAcc = math.floor(math.fabs(math.log10(interceptStep)))+2
        #~ self.interceptValue.setDecimals(interceptAcc)
        #~ self.interceptLBValue.setDecimals(interceptAcc)
        #~ self.interceptUBValue.setDecimals(interceptAcc)
        #~ 

        # now set initial values
        self.slopeValue.setValue(self._slopeDisplay)
        self.interceptValue.setValue(self._interceptDisplay)

        # and now the boundaries -- as valid for the slider
        # slope:
        self.slopeLBValue.setValue(self._slopeBounds[0])
        self.slopeUBValue.setValue(self._slopeBounds[1])
        # intercept
        self.interceptLBValue.setValue(self._interceptBounds[0])
        self.interceptUBValue.setValue(self._interceptBounds[1])

        self.updateFit.emit()


    def _interceptScaler(self, val):
        valuewidth = self.interceptUBValue.value() - self.interceptLBValue.value()
        currentVal = (self.interceptSlider.minimum() + val * self.interceptSlider.singleStep())/(self.interceptSlider.maximum() - self.interceptSlider.minimum())
        self.interceptValue.setValue(self.interceptLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def _slopeScaler(self, val):
        valuewidth = self.slopeUBValue.value() - self.slopeLBValue.value()
        currentVal = (self.slopeSlider.minimum() + val * self.slopeSlider.singleStep())/(self.slopeSlider.maximum() - self.slopeSlider.minimum())
        self.slopeValue.setValue(self.slopeLBValue.value() + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(intercept=self.interceptValue.value(), slope=self.slopeValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = { self._model.prefix :
                    { 'modeltype': 'linearModel',
                     'intercept' : {'value' : self.interceptValue.value(), 'vary': (not self.interceptFixedCB.isChecked()) },
                     'slope' : {'value' : self.slopeValue.value(), 'vary': (not self.slopeFixedCB.isChecked()) },
                    }
                }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model



class quadratic(QuadraticModel):
    def __init__(self, **kwargs):
        super(quadratic, self).__init__(**kwargs)

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("quadraticModel", self, "ui/quadraticModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        return super(quadratic, self).guess(data, **kw)        



class QuadraticParameterSettingDialog(ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(QuadraticParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)
        self.aSlider.valueChanged.connect(self._aScaler)
        self.bSlider.valueChanged.connect(self._bScaler)
        self.cSlider.valueChanged.connect(self._cScaler)
        self._modelName = modelname
        self._model = model
        self._model.prefix = "m" + str(self._index) + "_"
        self._parameters = None
        self.guessStartValuesBtn.clicked.connect(print)
        self.configDonePushBtn.clicked.connect(self._guessingDone)

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # first basic calculations 
        self._aDisplay = float(np.mean(self._ydata))
        self._aBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))
        self._bDisplay = float(np.mean(self._ydata))/float(np.mean(self._xdata))
        self._bBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))
        self._cDisplay = float(np.mean(self._ydata))/math.sqrt(np.mean(self._xdata))
        self._cBounds = (-10.*float(self._cDisplay), 10.*float(self._cDisplay))

        # first fix the accuracy of the display
        # number of steps;
        aStep =(self._aBounds[1] - self._aBounds[0])/(self.aSlider.maximum()-self.aSlider.minimum())
        aAcc = math.floor(math.fabs(math.log10(aStep)))+2
        self.aValue.setDecimals(aAcc)
        self.aLBValue.setDecimals(aAcc)
        self.aUBValue.setDecimals(aAcc)

        bStep =(self._bBounds[1] - self._bBounds[0])/(self.bSlider.maximum()-self.bSlider.minimum())
        bAcc = math.floor(math.fabs(math.log10(bStep)))+2
        self.bValue.setDecimals(bAcc)
        self.bLBValue.setDecimals(bAcc)
        self.bUBValue.setDecimals(bAcc)

        cStep =(self._cBounds[1] - self._cBounds[0])/(self.cSlider.maximum()-self.cSlider.minimum())
        cAcc = math.floor(math.fabs(math.log10(cStep)))+2
        self.cValue.setDecimals(cAcc)
        self.cLBValue.setDecimals(cAcc)
        self.cUBValue.setDecimals(cAcc)
        

        # now set initial values
        self.aValue.setValue(self._aDisplay)
        self.bValue.setValue(self._bDisplay)
        self.cValue.setValue(self._cDisplay)

        # and now the boundaries -- as valid for the slider
        # a:
        self.aLBValue.setValue(self._aBounds[0])
        self.aUBValue.setValue(self._aBounds[1])
        # b
        self.bLBValue.setValue(self._bBounds[0])
        self.bUBValue.setValue(self._bBounds[1])
        # c
        self.cLBValue.setValue(self._cBounds[0])
        self.cUBValue.setValue(self._cBounds[1])

        self.updateFit.emit()

    def _aScaler(self, val):
        valuewidth = self._aBounds[1]-self._aBounds[0]
        currentVal = (self.aSlider.minimum() + float(val * self.aSlider.singleStep()))/(self.aSlider.maximum() - self.aSlider.minimum())
        self.aValue.setValue(self._aBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _bScaler(self, val):
        valuewidth = self._bBounds[1]-self._bBounds[0]
        currentVal = (self.bSlider.minimum() + float(val * self.bSlider.singleStep()))/(self.bSlider.maximum() - self.bSlider.minimum())
        self.bValue.setValue(self._bBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def _cScaler(self, val):
        valuewidth = self._cBounds[1]-self._cBounds[0]
        currentVal = (self.cSlider.minimum() + float(val * self.cSlider.singleStep()))/(self.cSlider.maximum() - self.cSlider.minimum())
        self.cValue.setValue(self._cBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(a=self.aValue.value(), b=self.bValue.value(), c=self.cValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = { self._model.prefix :
                    { 'modeltype': 'quadraticModel',
                     'a' : {'value' : self.aValue.value(), 'vary': (not self.aFixedCB.isChecked()) },
                     'b' : {'value' : self.bValue.value(), 'vary': (not self.bFixedCB.isChecked()) },
                     'c' : {'value' : self.cValue.value(), 'vary': (not self.cFixedCB.isChecked()) } 
                    }
                }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model



class constant(ConstantModel):
    def __init__(self, **kwargs):
        super(constant, self).__init__(**kwargs)    

    def getWidget(self, xdata=None, ydata=None, index=None):
        self._widget = modelWidgeteer("constantModel", self, "ui/constantModelFitParameters.ui", xdata, ydata, index)
        return self._widget

    def guess(self, data, **kw):
        return super(constant, self).guess(data, **kw)        


class ConstantParameterSettingDialog(ParameterSettingDialog):

    def __init__(self, modelname, xdata, ydata, model=None, **kw):
        super(ConstantParameterSettingDialog, self).__init__(**kw)
        self.passData(xdata, ydata)

        self.constSlider.valueChanged.connect(self._constScaler)
        self._modelName = modelname
        self._model = model
        self._model.prefix = "m" + str(self._index) + "_"
        self._parameters = None
        self.guessStartValuesBtn.clicked.connect(print)
        self.configDonePushBtn.clicked.connect(self._guessingDone)

    def _guessingDone(self, **kw):
        self.guessingDone.emit()
        self.close(**kw)

    def update(self):
        # first basic calculations 
        self._constDisplay = float(np.mean(self._ydata))
        self._constBounds = (float(np.amin(self._ydata)), float(np.amax(self._ydata)))

        # first fix the accuracy of the display
        # number of steps;
        constStep =(self._constBounds[1] - self._constBounds[0])/(self.constSlider.maximum()-self.constSlider.minimum())
        constAcc = math.floor(math.fabs(math.log10(constStep)))+2
        self.constValue.setDecimals(constAcc)
        self.constLBValue.setDecimals(constAcc)
        self.constUBValue.setDecimals(constAcc)

        # now set initial value
        self.constValue.setValue(self._constDisplay)

        # and now the boundaries -- as valid for the slider
        self.constLBValue.setValue(self._constBounds[0])
        self.constUBValue.setValue(self._constBounds[1])

        self.updateFit.emit()

    def _constScaler(self, val):
        valuewidth = self._constBounds[1]-self._constBounds[0]
        currentVal = (self.constSlider.minimum() + float(val * self.constSlider.singleStep()))/(self.constSlider.maximum() - self.constSlider.minimum())
        self.constValue.setValue(self._constBounds[0] + currentVal*valuewidth)
        self.updateFit.emit()

    def getCurrentFitData(self):
        self._parameters = self._model.make_params(c=self.constValue.value())
        return self._model.eval(self._parameters, x=self._xdata)

    def automaticGuess(self):
        print("i'm guessing by the book")

    def getCurrentParameterDict(self):
        pdict = { self._model.prefix :
                    { 'modeltype': 'constantModel',
                     'c': {'value' : self.constValue.value(), 'vary': ( not self.constFixedCB.isChecked()) },
                    }
                }
        return pdict

    def getName(self):
        return self._modelName

    def getModel(self):
        return self._model


FitModels = { "constantModel" : constant,
              "linearModel" : linear,
              "quadraticModel" : quadratic,
              "gaussianModel" : gaussian,
              "lorentzianModel" : lorentzian,
              #~ "psvModel" : psv,
            }

