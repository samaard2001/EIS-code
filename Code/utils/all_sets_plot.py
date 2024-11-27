import matplotlib.pyplot as plt 

def plot_all_sets(name, parametre, calc_func, optimize_func): 
    fig, ax = plt.subplots(figsize=(10, 10)) 
    #ax.scatter(np.array(get_exp_data(i, "")[0][0]), -np.array(get_exp_data(i, "")[0][1]), label=f"Experimental", color = 'red') 
    for k in range(1, 5): 
        dic_elems, final_diff, frequencies, list_elems = optimize_func(k, parametre, calc_func)
        Z = calc_func(list_elems, frequencies)
        ax.plot(Z.real, -Z.imag, label = f'data set '+str(k))
    plt.legend()
    plt.xlabel('Real(Z) [Ω]')
    plt.ylabel('Imaginary(Z) [Ω]')
    plt.title(name+" ECM for data sets 1-4") 
    plt.show()