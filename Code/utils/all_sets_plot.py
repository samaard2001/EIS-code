import matplotlib.pyplot as plt 
import numpy as np
from utils.load_data import get_exp_data

def plot_all_sets(name, parametre, calc_func, optimize_func): 
    fig, ax = plt.subplots(figsize=(10, 10)) 
    #ax.scatter(np.array(get_exp_data(i, "")[0][0]), -np.array(get_exp_data(i, "")[0][1]), label=f"Experimental", color = 'red') 
    for k in range(1, 5): 
        frequencies = np.array(get_exp_data(k, "")[1])
        final_diff, list_elems = optimize_func(k, parametre, calc_func)
        Z = calc_func(list_elems, frequencies)
        ax.plot(Z.real, -Z.imag, label = f'data set '+str(k))
    plt.legend()
    plt.xlabel(r"Z' [$\Omega$]")
    plt.ylabel(r"-Z'' [-$\Omega$]")
    plt.title(name+" ECM for data sets 1-4") 
    plt.show()