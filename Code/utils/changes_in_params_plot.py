import matplotlib.pyplot as plt 
from utils.convertion import dict_to_list, list_to_dict

def finding_params(parametre, calc_func, optimize_func): 
    dic_list = []
    for l in range(1,5):
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
    combined_dict = finding_params(parametre, calc_func, optimize_func)
    x = [1, 2, 3, 4]
    fig, ax = plt.subplots(figsize=(6, 6)) 
    for key in key_list: 
        ax.scatter(x, combined_dict[key], label = key)

    plt.legend()
    plt.xlabel("Data Set Number")
    plt.ylabel("Parameter Value")
    plt.title("Change in Parameters") 
    plt.show()
