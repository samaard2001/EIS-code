import numpy as np 
from utils.load_data import get_exp_data
from utils.convertion import dict_to_list, list_to_dict
from scipy.optimize import minimize


# Optimizing the difference function for a given data set i 
def optimize_diff(i, parametre, calc_func):
    '''
    Optimizing the difference function by minimizing the sum of square error difference for a given data set i. 
    The algorithm used is scipy.minimize.
    
    '''
    # Load the experimental data 
    exp_real = np.array(get_exp_data(i, "")[0][0])
    exp_imag = np.array(get_exp_data(i, "")[0][1])
    frequencies = np.array(get_exp_data(i, "")[1])

    # Difference function for the optimization
    def diff_func(comp, exp_real, exp_imag, frequencies):
        Z = calc_func(comp, frequencies)
        diff_real = Z.real - exp_real
        diff_imag = Z.imag - exp_imag
        sum_square_diff = np.sum(diff_real ** 2 + diff_imag ** 2)
        return sum_square_diff

    # Convert initial dictionary to list for optimization
    initial_elems = dict_to_list(parametre)

    # Optimization options
    options = {
        'maxiter': 10000,    
        'ftol': 1e-4,      
    }

    # Minimize the difference function (optimize parameters)
    opt = minimize(diff_func, initial_elems, args=(exp_real, exp_imag, frequencies), method='TNC', options=options)
    opt_elems = list_to_dict(parametre, opt.x)
    final_diff = diff_func(opt.x, exp_real, exp_imag, frequencies)

    return final_diff, opt.x 

