import numpy as np
import pyswarms as ps 
from pyswarms.single import GlobalBestPSO
from utils.load_data import get_exp_data
from utils.convertion import dict_to_list, list_to_dict

def pso(i, parametre, calc_func): 
   
   '''
   Optimizing the difference function by minimizing the sum of square error difference for a given data set i. 
   The algorithm used is Particle Swarm Optimization.
   '''

   exp_real = np.array(get_exp_data(i, "")[0][0])
   exp_imag = np.array(get_exp_data(i, "")[0][1])
   frequencies = np.array(get_exp_data(i, "")[1])

   #lower_bounds = [ ] 
   #upper_bounds = [] 
   #bounds = (lower_bounds, upper_bounds)

   initial_elems = dict_to_list(parametre)

   def diff_func(comp, exp_real, exp_imag, frequencies):
           Z = calc_func(comp, frequencies)
           diff_real = Z.real - exp_real
           diff_imag = Z.imag - exp_imag
           sum_square_diff = np.sum(diff_real ** 2 + diff_imag ** 2)
           return sum_square_diff

   def wrapped_diff_function(params):
           return np.array([diff_func(param_set, exp_real, exp_imag, frequencies) for param_set in params])

   n_dim = 10 # changing 10 parameters

   options = {'c1': 0.5,      # Cognitive parameter (influence of personal best)
       'c2': 0.3,      # Social parameter (influence of global best)
       'w': 0.9,       # Inertia parameter (how much particles retain velocity)
       }

   optimizer = ps.single.GlobalBestPSO(n_particles=200, dimensions=n_dim, options=options) #, bounds=bounds)

   best_cost, best_params = optimizer.optimize(wrapped_diff_function, iters=200)
   return best_cost, best_params