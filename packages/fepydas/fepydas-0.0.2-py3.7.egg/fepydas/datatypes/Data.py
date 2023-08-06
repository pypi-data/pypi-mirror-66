#!/usr/bin/python3
import numpy
from fepydas.libs.deconvolution import deconvolve, deconvolve2D

class DataType:
  def __init__(self, name: str, unit:str):
    self.name = name
    self.unit = unit

class Data:
  def __init__(self, values: numpy.ndarray, datatype: DataType):
    self.values = values
    self.datatype = datatype

  def normalize(self):
    self.values = self.values / numpy.max(self.values)
  
  def divideBy(self, data):
    self.values = self.values/data

class Data1D(Data):
  def __init__(self, values: numpy.ndarray, datatype: DataType):
    super().__init__(values,datatype)

  def deconvolve(self,ref,eps=None):
    self.values = deconvolve(self.values, ref.values,eps)

  def cutAndGetIndexRange(self, min, max):
    idx1, idx2 = self.getIndexRange(min,max)
    self.cut(idx1,idx2)
    return idx1, idx2 

  def getIndexRange(self, min, max):
    idx1 = (numpy.abs(self.values - min)).argmin()
    idx2 = (numpy.abs(self.values - max)).argmin()
    if idx2<idx1:
      temp = idx2
      idx2 = idx1
      idx1 = temp
    return idx1,idx2

  def cut(self, idx1, idx2):
    self.values = self.values[idx1:idx2]
 
  def shiftValues(self, amount):
    self.values += amount

class Data2D(Data):
  def __init__(self, values: numpy.ndarray, datatype: DataType):
    super().__init__(values,datatype)

  def average(self):
    return Data1D(numpy.average(self.values,axis=0),self.datatype)

  def collapse(self, filter=None):
    if filter:
      return Data1D(numpy.sum(self.values[filter],axis=0), self.datatype)
    else:
      return Data1D(numpy.sum(self.values,axis=0),self.datatype)

  def deconvolve(self,ref,eps=None):
    self.values = deconvolve2D(self.values, ref.values,eps)

  def integrate(self):
    return Data1D(numpy.sum(self.values,axis=1),self.datatype)

  def normalizeIndividual(self):
    maxima = numpy.max(self.values,axis=1)
    self.values = (self.values.T / maxima).T

  def cut(self, idx1, idx2):
    self.values = self.values[:,idx1:idx2]

class Data3D(Data):
  def __init__(self, values: numpy.ndarray, datatype: DataType):
    super().__init__(values,datatype)

  def cutMap(self, xMin, xMax, yMin, yMax):
    self.values = self.values[xMin:xMax,yMin:yMax,:]

  def getIndexRange(self, xMin, xMax, yMin, yMax):
    idx1 = (numpy.abs(self.values[:,0,0] - xMin)).argmin(axis=0)
    idx2 = (numpy.abs(self.values[:,0,0] - xMax)).argmin(axis=0)
    idx3 = (numpy.abs(self.values[0,:,1] - yMin)).argmin(axis=0)
    idx4 = (numpy.abs(self.values[0,:,1] - yMax)).argmin(axis=0)  
    return idx1,idx2,idx3,idx4

  def cutAndGetIndexRange(self, xMin, xMax, yMin, yMax):
    i1,i2,i3,i4 = self.getIndexRange(xMin,xMax,yMin,yMax)
    self.cutMap(i1,i2,i3,i4)
    print(i1,i2,i3,i4)
    return i1,i2,i3,i4

  def integrate(self):
    return Data2D(numpy.sum(self.values, axis=2), self.datatype)

  def average(self):
    return Data1D(numpy.average(self.values, axis=(0,1)), self.datatype)

  def extractAxes(self):
    y = self.values[0,:,1]
    x = self.values[:,0,0]
    return Data1D(x, self.datatype), Data1D(y, self.datatype)
  
  def cut(self, idx1, idx2):
    self.values = self.values[:,:,idx1:idx2]

    
class Transformation():
  def __init__(self, function, parameterDict):
    self.function = function
    self.params = parameterDict

  def apply(self, values):
    return self.function(values,**self.params)

class Response():
  def __init__(self, input: Data1D, values: Data1D):
    self.input = input
    self.values = values 

  def interpolateResponse(self, inputValues: numpy.ndarray, zeroFloor=False):
    if zeroFloor:
      self.values.values -= numpy.amin(self.values.values)*0.9
    return numpy.interp(inputValues, self.input.values, self.values.values)
