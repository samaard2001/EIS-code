import numpy as np 
from scipy.optimize import minimize
from utils.convertion import dict_to_list, list_to_dict 
from utils.optimize import optimize_diff 
from utils.load_data import get_exp_data 
from utils.Z_randles import calc_randles_Z, a_randles 

# Optimizing the difference function for a given data set i 
def optimize_randles(i, parametre, calc_func):
    '''
    Optimizing the difference function by minimizing the sum of square error difference for a given data set i, 
    by fitting to the fitted ECM.  
    The algorithm used is scipy.minimize.
    '''
    final_diff_randles, list_randles_Z = optimize_diff(i, a_randles, calc_randles_Z)
    frequencies = np.array(get_exp_data(i, "")[1])

    # Difference function for the optimization
    def diff_func(comp, list_randles_Z, frequencies):
        Z_randles = calc_randles_Z(list_randles_Z, frequencies)
        Z_meyers = calc_func(comp, frequencies)
        diff = Z_meyers - Z_randles
        sum_square_diff = np.sum(diff**2)
        return sum_square_diff

    # Convert initial dictionary to list for optimization
    initial_elems = dict_to_list(parametre)

    # Optimization options
    options = {
        'maxiter': 10000,    
        'ftol': 1e-4,      
    }

    # Minimize the difference function (optimize parameters)
    opt = minimize(diff_func, initial_elems, args=(list_randles_Z, frequencies), method='TNC', options=options)
    opt_elems = list_to_dict(parametre, opt.x)
    final_diff = diff_func(opt.x, list_randles_Z, frequencies)

    return final_diff, opt.x 
