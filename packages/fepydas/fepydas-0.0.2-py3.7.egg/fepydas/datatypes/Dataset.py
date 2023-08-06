#!/usr/bin/python3
import numpy
import pickle
from fepydas.datatypes.Data import Data, Data1D, Data2D, Data3D, Response
from fepydas.datatypes import NUMBER
from fepydas.libs.fitting import extractCalibration
from fepydas.libs.deconvolution import trimRef
from fepydas.libs.clustering import performGMM
from fepydas.workers.Fit import LimitedGaussianFit, CalibrationFit, Fit, LinearFit
from fepydas.workers.ASCIIWriter import MultiSpectrumWriter


class BaseDataset:
  def saveBinary(self, filename):
    f = open(filename,"bw")
    pickle.dump(self,f)
    f.close()

class Dataset(BaseDataset):
  def __init__(self, axis: Data1D, data: Data):
    self.axis = axis
    self.data = data

  def applyAxisTransformation(self, transformation):
    self.axis.values = transformation.apply(self.axis.values)
    print("Applied Axis Transformation")

  def cutAxis(self, minVal, maxVal):
    idx1, idx2 = self.axis.cutAndGetIndexRange(minVal,maxVal)
    self.data.cut(idx1,idx2)

  def divideBySpectrum(self, spectrum):
    self.data.divideBy(spectrum.data.values)

class Spectrum(Dataset):
  def __init__(self, axis: Data1D, data: Data1D):
    super().__init__(axis,data)

  def export(self,filename):
    msw = MultiSpectrumWriter(filename)
    msw.addSpectrum(self)
    msw.write()
    
  def normalize(self):
    self.data.normalize()

class SpectrumSeries(Dataset):
  def __init__(self, axis:Data1D, data:Data2D):
    super().__init__(axis,data)


  def __init__(self, spectra, interpol=False, names=None):
    if interpol:
      valmin, mins, maxs, res = [], [],[],[]
      for i in range(len(spectra)):
        mins.append(numpy.amin(spectra[i].axis.values))
        maxs.append(numpy.amax(spectra[i].axis.values))
        res.append(numpy.average(numpy.diff(spectra[i].axis.values)))
        if res[i] < 0: #axis must be ascending
          spectra[i].axis.values = numpy.flip(spectra[i].axis.values)
          spectra[i].data.values = numpy.flip(spectra[i].data.values)
        valmin.append(numpy.amin(spectra[i].data.values))
      resolution = numpy.abs(numpy.average(res))
      min, max = numpy.amin(mins), numpy.amax(maxs)
      valmin = numpy.amin(valmin)
      #Interpolation, set non-overlapping regions to minimum so weight will be 0
      newAxis = Data1D(numpy.linspace(min, max, int((max-min)/resolution)), spectra[0].axis.datatype)
      data = Data2D(numpy.zeros((len(spectra),len(newAxis.values))), spectra[0].data.datatype)
      for i in range(len(spectra)):
        data.values[i,:] = numpy.interp(newAxis.values, spectra[i].axis.values, spectra[i].data.values, left=valmin, right=valmin) - valmin +1
      super().__init__(newAxis,data)
    else:
      data = Data2D(numpy.zeros((len(spectra),len(spectra[0].data.values))), spectra[0].data.datatype)
      for i in range(len(spectra)):
        data.values[i,:] = spectra[i].data.values
      #TODO check AXIS consistency
      super().__init__(spectra[0].axis, data)
    #TODO default create keys in SS init
    if names:
      self.keys = Data1D(names, NUMBER)
    else:
      self.keys = Data1D(range(len(spectra)),NUMBER)
  
  def average(self):
    return Spectrum(self.axis, self.data.average())

  def collapse(self, filter=None):
    return Spectrum(self.axis, self.data.collapse(filter))

  def collapseDominatingCluster(self, maxClusters = None):
    averages, cluster, resp = performGMM(self.data.values, maxClusters=maxClusters)
    print(averages[1]-averages[0])
    dominatingCluster = numpy.bincount(cluster).argmax()
    keep = numpy.where(cluster==dominatingCluster)
    return self.collapse(filter=keep)

  def highDynamicRange(self):
    #calculate weights
    zmax, zmin = (numpy.amax(self.data.values)*0.99) , (numpy.amin(self.data.values))
    zceil = numpy.full_like(self.data.values, zmax)
    zcenter, zrange = (zmax+zmin)/2, (zmax-zmin)/2
    weights =(zrange - numpy.abs((numpy.minimum(self.data.values,zceil)) - zcenter)) #Low weight for low (under-exposed) or high (over-exposed) values, high weight for medium values

    #calculate mappings
    num = len(self.keys.values)
    crossweights = numpy.zeros((num,num,len(self.data.values[0,:])))
    for i in range(num):
      for j in range(num):
        crossweights[i,j,:] = numpy.multiply(weights[i,:],weights[j,:])
    integratedCWs = numpy.sum(crossweights, axis=2)
    idxs = numpy.flip(numpy.argsort(numpy.sum(integratedCWs, axis=1)))
  
    
    def linearProjection(dataIn, dataRef, crossweights):
      return dataIn*numpy.average(dataRef/dataIn, weights=crossweights)

    mapped = numpy.zeros((num))
    mapped[idxs[0]] = 1

    for i in range(len(idxs)-1):
      idx = idxs[i+1]
      usableCWs = numpy.multiply(integratedCWs[idx,:],mapped)
      best = numpy.argsort(usableCWs)[-1]
      self.data.values[idx,:] = linearProjection(self.data.values[idx,:],self.data.values[best,:], crossweights[idx,best,:])
      print("mapped",idx,"to",best)
      mapped[idx]=1

    return Spectrum(self.axis, Data2D(numpy.average(self.data.values, axis=0, weights=weights),self.data.datatype))

  def integrate(self):
    return Spectrum(self.keys, self.data.integrate())
  
  def normalize(self, individual=False):
    if individual:
      self.data.normalizeIndividual()
    else:
      self.data.normalize()

  def subtractBaseline(self):
    #Invoke only if no dark spectrum available!
    baseline = numpy.min(self.data.values)-1
    self.data.values-=(baseline)
    print("Baseline removed: {0}".format(baseline))

class Map(BaseDataset):
  def __init__(self, mapping:Data3D, data:Data2D):
    self.mapping = mapping
    self.data = data

    

class SpectrumSeriesWithCalibration(SpectrumSeries):
  def __init__(self, axis: Data1D, data:Data2D, calibration: Data1D):
    super().__init__(axis,data)
    self.calibrated = False
    self.calibration = calibration

  def calibrate(self, references, width=10):
    transformation = extractCalibration(self.axis, self.calibration, references, width=width)
    self.applyAxisTransformation(transformation)
    print("Calibrated")

class SpectrumMap(SpectrumSeriesWithCalibration):
  def __init__(self, axis: Data1D, data:Data3D, mapping:Data3D, calibration: Data1D):
    super().__init__(axis,data,calibration)
    self.mapping = mapping
    #TODO
  def integrate(self):
    return Map(self.mapping, self.data.integrate())

  def average(self):
    return Spectrum(self.axis, self.data.average())

  def maximum(self):
    return Map(self.mapping, Data3D(self.axis.values[numpy.argmax(self.data.values,axis=2)],self.axis.datatype))

  def cutMap(self, xMin, xMax, yMin, yMax):
    i1,i2,i3,i4 = self.mapping.cutAndGetIndexRange(xMin,xMax,yMin,yMax)
    self.data.cutMap(i1,i2,i3,i4)

  def fit(self, fitter:Fit):
    x, y, z = self.data.values.shape
    batchData = self.data.values.reshape(x*y,z)
    fitter.batchFit(self.axis.values, batchData)
    
  def fitParameterToMap(self, fitter, paramName, paramDatatype):
    x, y, z = self.data.values.shape
    vals = numpy.ndarray(shape=(x*y))
    print(fitter.results.shape)
    for i, result in enumerate(fitter.results):
      if result==0:
        vals[i] = 0
      else:
        print(result)
        vals[i] = result.params[paramName].value
    values = Data2D(vals.reshape(x,y), paramDatatype)
    return Map(self.mapping, values)


class PLE(SpectrumSeriesWithCalibration):
  def __init__(self, axis: Data1D, keys:Data1D, data:Data2D, calibration: Data1D, response: Response):
    super().__init__(axis,data,calibration)
    self.keys = keys
    self.response = response
  
  def applyLampResponseCorrection(self,zeroFloor=False):
    print(self.response.values.values)
    interpolatedResponse = self.response.interpolateResponse(self.keys.values,zeroFloor)
    for i in range(len(self.keys.values)):
      self.data.values[i] /= interpolatedResponse[i]
    print("Lamp Response Correction made")
    
  def calibrateLamp(self,width=2,thresh=1):
    fit = LimitedGaussianFit()
    nominal = []
    fitted = []
    fittedErrs = []
    for i in range(len(self.keys.values)):
      x, y = fit.initializeAutoLimited(self.axis.values,self.data.values[i],self.keys.values[i],width,thresh)
      if type(x) is numpy.ndarray and len(x)>40:
        #print(x,y)
        fit.fit(x,y)
        nominal.append(self.keys.values[i])
        fitted.append(fit.result.params["x0"].value)
        fittedErrs.append(fit.result.params["x0"].stderr)
    nominal = numpy.array(nominal,dtype=numpy.float64)
    fitted = numpy.array(fitted,dtype=numpy.float64)
    print(nominal,fitted,fittedErrs)
    calib = CalibrationFit()
    calib.intializeAuto()
    calib.fit(nominal,fitted)#,peakErrs)
    print(calib.result.params)
    transformation = calib.toTransformation()
    self.keys.values = transformation.apply(self.keys.values)
    print("Calibrated Lamp")
    return transformation

class SpectrumWithIRF(Spectrum):
  def __init__(self, axis: Data1D, data: Data, IRF: Data1D):
    super().__init__(axis,data)
    self.trimIRF(IRF)

  def evaluateConvolutionFit(self, fit):
    return Data1D(fit.evaluateConvolution(self.axis.values, self.IRF.values), self.data.datatype)

  def getExtendedIRF(self):
    data = numpy.zeros(self.data.values.shape)
    for i,x in enumerate(self.IRF.values):
      data[self.IRFStart+i]=x
    return data/data.max()

  def trimIRF(self,IRF):
    self.IRFStart = 0#lastZero+1
    IRF.values = trimRef(IRF.values)
    self.IRF = IRF
     
  def deconvolve(self,eps=None):
    self.data.deconvolve(self.IRF,eps)

class SpectraWithCommonIRF(SpectrumWithIRF):
  def __init__(self, axis: Data1D, data: Data2D, IRF: Data1D, identifiers: Data1D):
    super().__init__(axis,data,IRF)
    self.keys = identifiers

  def normalize(self, individual=False):
    if individual:
      self.data.normalizeIndividual()
    else:
      self.data.normalize()
