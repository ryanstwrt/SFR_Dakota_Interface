#!/usr/bin/env python
import scipy.interpolate
import h5py
import pandas as pd
import os
import pickle
#import dill as pickle

#import dakota.interfacing as di
#params, results = di.read_parameters_file(parameters_file='sfr_moo.in', results_file='sfr_moo.out')

###Hard Coded In Values - need to fix

#params = {'height': (50, 70), 'smear': (50, 70)}
#results = ['keff', 'void_coeff', 'doppler_coeff']

db = h5py.File('test_db.h5', 'r+')
reactorDict = {}
for r in db.keys():
  reactor = db[r]
  labels = [attr for attr in reactor.attrs]
  attrs = [reactor.attrs[attr] for attr in reactor.attrs]
  dataDict = dict(zip(labels, attrs))
  reactorDict[r] = dataDict

reactorData = pd.DataFrame(reactorDict)
reactorData = reactorData.T
# Convert stored bytes back to strings
reactorData['enrichment'] = reactorData['enrichment'].apply(lambda x : x.decode("utf-8"))
reactorData['condition'] = reactorData['condition'].apply(lambda x : x.decode("utf-8"))

reactorData.to_pickle("./sfr_Data.pkl")

# Create a a coordinate system via the variables for interpolator
#var_array = []
#for k, v in params.items():
#  var_list = []
#  for data_point in reactorData[k]:
#    var_list.append(data_point)
#  var_array.append(var_list)
#coordinates = list(zip(*var_array))
#  
## Create a list of objectives to solve for, and a list of known values
## for the objectives 
#obj_dict = {}
#interp = {}
#for obj in results:
#  obj_list = []
#  for data_point in reactorData[obj]:
#    try:
#      obj_list.append(data_point[0])
#    except IndexError:
#      obj_list.append(data_point)
#  obj_dict[obj] = obj_list
#  
## Create a dictionary of the objective function and the interpolator,
## given the coordinates and objective values
#for obj_name, obj in obj_dict.items():
#  interp[obj_name] = scipy.interpolate.LinearNDInterpolator(coordinates, obj)
#  
#fileObject = open('interpolator.pkl', 'wb')
#
#pickle.dump(interp, fileObject)
#fileObject.close()

os.system("dakota -i sfr_moo.in -o sfr.out > sft.stdout")