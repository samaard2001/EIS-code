import numpy as np
import pyswarms as ps 
from pyswarms.single import GlobalBestPSO
from utils.load_data import get_exp_data
from utils.convertion import dict_to_list, list_to_dict

def pso(i, parametre, calc_func): 

   exp_real = np.array(get_exp_data(i, "")[0][0])
   exp_imag = np.array(get_exp_data(i, "")[0][1])
   frequencies = np.array(get_exp_data(i, "")[1])

   #lower_bounds = [0, 0, 0, 0, 0, 0, 0, 1e-20, 0, 1e4, ] 
   #upper_bounds = [0.002, 0.03, 0.03, 3, 3, 1, 1, 1e-15, 1, 1e8] 
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

#sol = basinhopping(diff_func, x0=initial_elems, niter=200, T=1, stepsize=0.2, minimizer_kwargs={'method':'slsqp', 'args':(exp_real, exp_imag, frequencies), 'bounds':bounds, 'tol':10**-6}, take_step=None, accept_test=None, callback=None, interval=50, disp=True, niter_success=None, seed=None)
#sol_elems = list_to_dict(a_fitting, sol.x)