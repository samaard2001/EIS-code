import numpy as np 
import matplotlib.pyplot as plt 
from utils.convertion import dict_to_list, list_to_dict
from utils.load_data import get_exp_data
from utils.optimize import optimize_diff
from utils.check_SOC import get_vdc


def optimizing_plot(i, name, a_params, calc_func, diff_func): 
    '''
    Plotting the experimental Nyquist plot, the original simulation and the fitted simulation. 
    '''
    frequencies = np.array(get_exp_data(i, "")[1])
    Z = calc_func(dict_to_list(a_params), frequencies)

    final_diff, list_elems = diff_func(i, a_params, calc_func)
    Z_scipy = calc_func(list_elems, frequencies)

    fig, ax = plt.subplots(figsize=(6, 6)) 
    ax.scatter(np.array(get_exp_data(i, "")[0][0]), -np.array(get_exp_data(i, "")[0][1]), color = 'red', label=f"Experimental "+str(np.round(get_vdc(i, ""),3))+" V") 
    ax.scatter(Z.real, -Z.imag, label = f'ECM '+name, color = 'blue')
    ax.plot(Z_scipy.real, -Z_scipy.imag, label = f'scipy', color = 'green')
    plt.legend()
    plt.title("Comparing") 
    plt.show() 