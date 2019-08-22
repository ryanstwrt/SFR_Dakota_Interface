#!/usr/bin/env python

# Dakota will execute this script as
#   rosenbrock_bb_di.py params.in results.out
#  The command line arguments will be extracted by dakota.interfacing automatically.

# necessary python modules
import dakota.interfacing as di

# ----------------------------
# Parse Dakota parameters file
# ----------------------------

params, results = di.read_parameters_file()

# -------------------------------
# Convert and send to application
# -------------------------------

# execute the rosenbrock analysis as a separate Python module
print("Running ROM Interpolator...")
from rom_solver import interpolate_objective_functions
interp_results = interpolate_objective_functions(params, results)
print("ROM Interpolator Copmlete.")


# ----------------------------
# Return the results to Dakota
# ----------------------------

# Insert functions from rosen into results
# Results.responses() yields the Response objects.
from rom_solver import fitness_function
fit_func, fitness = fitness_function(interp_results)

for i, r in enumerate(results.responses()):
  r.function = fit_func[r._descriptor]

results.write()
