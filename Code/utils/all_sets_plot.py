import matplotlib.pyplot as plt 
import numpy as np
from utils.load_data import get_exp_data

def plot_all_sets(name, parametre, calc_func, optimize_func): 

    '''
    Plots all experimental data sets and also the fitted model of your choice for each set. 
    
    Inputs: 
    name: specify which model you are plotting. 
    parametre: the parameter set in your model you want to optimize.
    calc_func: the function that calculates impedance from a given parameter set. 
    optimize_func: the function that minimizes the sum of square error difference 
    between the experimental and the model impedances. The function output is 
    an optimized parameter list for your model of choice. 

    '''
    fig, ax = plt.subplots(figsize=(10, 10)) 
    colors = ['red', 'blue', 'green', 'orange']
    for k in range(1, 5): 
        frequencies = np.array(get_exp_data(k, "")[1])
        exp_real = np.array(get_exp_data(k, "")[0][0])
        exp_imag = np.array(get_exp_data(k, "")[0][1])
        final_diff, list_elems = optimize_func(k, parametre, calc_func)
        Z = calc_func(list_elems, frequencies)

        color = colors[k - 1]
        label = f"Data set {k}" 

        ax.scatter(np.array(get_exp_data(k, "")[0][0]), -np.array(get_exp_data(k, "")[0][1]), color = color, label=label) 
        ax.plot(Z.real, -Z.imag, color = color)
    plt.legend()
    plt.xlabel(r"Z' [$\Omega$]")
    plt.ylabel(r"-Z'' [-$\Omega$]")
    plt.title("Experimental and fitted "+str(name)+" for data sets 1-4") 
    plt.show()