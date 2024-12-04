import matplotlib.pyplot as plt 
import seaborn as sns
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

def plot_change_param(key_list, parametre, calc_func, optimize_func): 

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
    x = [1, 2, 3, 4]

    sns.set(style="whitegrid")
    palette = sns.color_palette("tab10")  
    
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100) 
    
    for i, key in enumerate(key_list):
        ax.plot(x, combined_dict[key], label=key, 
                marker='o', linestyle='-', linewidth=1.5, markersize=6, 
                color=palette[i % len(palette)])
    
    ax.grid(visible=True, linestyle='--', alpha=0.7)
    ax.set_xlabel("Data Set Number", fontsize=12)
    ax.set_ylabel("Parameter Value", fontsize=12)
    ax.set_title("Change in Parameters", fontsize=14, weight='bold')
    ax.legend(title="Parameters", fontsize=10, title_fontsize=11, loc='best')
    
    plt.tight_layout()  
    plt.show()
