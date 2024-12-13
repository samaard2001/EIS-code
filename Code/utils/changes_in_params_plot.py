import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.gridspec import GridSpec
#import seaborn as sns
from utils.convertion import dict_to_list, list_to_dict



def finding_params(parametre, calc_func, optimize_func): 
    '''
    Combines the fitted parameters (from the model of your choice) for all datasets to a dictionary, 
    where each key is a parameter in the parameter set and the corresponding value is a list of 
    values. Each value in the list is the value of the parameter key for a data set i. 

    Inputs: 
    parametre: the parameter set in your model you want to optimize.
    calc_func: the function that calculates impedance from a given parameter set. 
    optimize_func: the function that minimizes the sum of square error difference 
    between the experimental and the model impedances. The function output is 
    an optimized parameter list for your model of choice. 

    '''
    dic_list = []
    for l in range(1, 5):
        final_diff, list_elems = optimize_func(l, parametre, calc_func)
        dic_elems = list_to_dict(parametre, list_elems)
        dic_list.append(dic_elems)
    
    combined_dict = {}
    
    for d in dic_list:
        for key, value in d.items():
            # If key is not in combined_dict, initialize with empty list
            if key not in combined_dict:
                combined_dict[key] = []
            # Append the value to the list for this key
            combined_dict[key].append(value)

    return combined_dict

def first_plot_change_param(key_list, name, unit, parametre, calc_func, optimize_func): 

    '''
    Plots the change in fitted (specicic) parameters from dataset to dataset.  

    Inputs: 
    key_list: the specific parameters in your parameter set you want to 
    observe change in. 
    parametre: the parameter set in your model you want to optimize.
    calc_func: the function that calculates impedance from a given parameter set. 
    optimize_func: the function that minimizes the sum of square error difference 
    between the experimental and the model impedances. The function output is 
    an optimized parameter list for your model of choice. 

    '''

    combined_dict = finding_params(parametre, calc_func, optimize_func)
    x = [0, 50, 100, 150]

    fig, ax = plt.subplots(figsize=(8, 6), dpi=100) 
    if len(key_list) == 1: 
        ax.plot(x, combined_dict[key_list[0]], 
                marker='o', linestyle='-', linewidth=1.5, markersize=6) 
                #color=palette[i % len(palette)])

    elif len(key_list) >= 1: 
        for i, key in enumerate(key_list):
            ax.plot(x, combined_dict[key], label=key, 
                    marker='o', linestyle='-', linewidth=1.5, markersize=6) #color=palette[i % len(palette)])
        ax.legend(title="Parameters", fontsize=10, title_fontsize=11, loc='best')
    
    #ax.grid(visible=True, linestyle='--', alpha=0.7)
    ax.set_xlabel("Number of Cycles")
    ax.set_title("Change in "+name)
    ax.set_ylabel(unit)
    plt.tight_layout()  
    plt.show()

def plot_change_param(parametre, calc_func, optimize_func): 

    '''
    Plots the change in fitted (specicic) parameters from dataset to dataset.  

    Inputs: 
    key_list: the specific parameters in your parameter set you want to 
    observe change in. 
    parametre: the parameter set in your model you want to optimize.
    calc_func: the function that calculates impedance from a given parameter set. 
    optimize_func: the function that minimizes the sum of square error difference 
    between the experimental and the model impedances. The function output is 
    an optimized parameter list for your model of choice. 

    '''

    combined_dict = finding_params(parametre, calc_func, optimize_func)
    x = [0, 50, 100, 150]

    #sns.set(style="whitegrid")
    #palette = sns.color_palette("tab10")

    fig = plt.figure(layout ='constrained', figsize = (12,12)) 
    gs = GridSpec(2,2,figure = fig)

    # Solution Resistance 
    ax_Rel = fig.add_subplot(gs[0,0])
    ax_Rel.set_ylabel(r"[$\Omega$]")
    ax_Rel.set_xlabel('Number of Cycles')
    ax_Rel.set_title("Change in Solution Resistance")

    # Charge Transfer Resistance
    ax_Rct = fig.add_subplot(gs[0,1])
    ax_Rct.set_ylabel(r"[$\Omega$]")
    ax_Rct.set_xlabel('Number of Cycles')
    ax_Rct.set_title("Change in Charge Transfer Resistances")
    key_Rct = ['R_ct1', 'R_ct2']

    # Capacitance
    ax_C = fig.add_subplot(gs[1,0])
    ax_C.set_ylabel(r"[F]")
    ax_C.set_xlabel('Number of Cycles')
    ax_C.set_title("Change in Capacitances")
    key_C = ['Q1', 'Q2']

    # Warburg Coefficient
    ax_A = fig.add_subplot(gs[1,1])
    ax_A.set_ylabel(r"[$\frac{\Omega}{\sqrt{s}}$]")
    ax_A.set_xlabel('Number of Cycles')
    ax_A.set_title("Change in Warburg Coefficient")

    # Plotting 
    ax_Rel.plot(x, combined_dict['R_el'],
                marker='o', linestyle='-', linewidth=1.5, markersize=6) #color=palette[i % len(palette)])
    ax_Rct.plot(x, combined_dict['R_ct1'], 
                marker='o', linestyle='-', linewidth=1.5, markersize=6) #color=palette[i % len(palette)])
    ax_Rct.plot(x, combined_dict['R_ct2'], 
                marker='o', linestyle='-', linewidth=1.5, markersize=6) #color=palette[i % len(palette)])
    ax_C.plot(x, combined_dict['Q1'], 
                marker='o', linestyle='-', linewidth=1.5, markersize=6) #color=palette[i % len(palette)])
    ax_C.plot(x, combined_dict['Q2'], 
                marker='o', linestyle='-', linewidth=1.5, markersize=6) #color=palette[i % len(palette)])
    ax_A.plot(x, combined_dict['A1'],
                marker='o', linestyle='-', linewidth=1.5, markersize=6) #color=palette[i % len(palette)])


    return plt.show()
