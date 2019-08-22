def interpolate_objective_functions(reactor_vars, obj_vars):
  """Utilize the scipy ND interpolator to solve for the objective functions."""
  import numpy as np
  import scipy.interpolate
  import h5py
  import pandas as pd
  import pickle

  reactorData = pd.read_pickle("./sfr_Data.pkl")

 # Create a a coordinate system via the variables for interpolator
  var_array = []
  for k, v in reactor_vars.items():
    var_list = []
    for data_point in reactorData[k]:
      var_list.append(data_point)
    var_array.append(var_list)
  coordinates = list(zip(*var_array))
 
 # Create a list of objectives to solve for, and a list of known values
 # for the objectives 
  obj_dict = {}
  interp = {}
  for obj in obj_vars:
    obj_list = []
    for data_point in reactorData[obj]:
      try:
        obj_list.append(data_point[0])
      except IndexError:
        obj_list.append(data_point)
    obj_dict[obj] = obj_list
 
  #fileObject = open('./interpolator.pkl', 'rb')
  #interp = pickle.load(fileObject)
  #fileObject.close()
  #Create a dictionary of the objective function and the interpolator,
  # given the coordinates and objective values
  for obj_name, obj in obj_dict.items():
    interp[obj_name] = scipy.interpolate.LinearNDInterpolator(coordinates, obj)

  #Use the interpolator to solve for the objective function given the reactor variables
  objective_function = {}
  for name, interpolator in interp.items():
    a = [x for x in reactor_vars.values()]
    objective_function[name] = float(interpolator(tuple(a)))

  return objective_function

def fitness_function(obj_fn):
  """Rudimentary fitness function for testing"""
  fitness_vec = {}
  keff_fn = -obj_fn['keff'] if obj_fn['keff'] > 1.05 else 10.0
  void_fn = obj_fn['void_coeff']/100 if obj_fn['void_coeff'] < -75 else 10.0
  doppler_fn = obj_fn['doppler_coeff'] if obj_fn['doppler_coeff'] < -0.5 else 10.0
  fitness_vec = {'keff': keff_fn, 'void_coeff': void_fn, 'doppler_coeff': doppler_fn}
  return(fitness_vec, sum(fitness_vec.values()))