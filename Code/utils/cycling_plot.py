import numpy as np 
import matplotlib.pyplot as plt 

def extract_data(dict): 
    U = []
    I = []
    time = []
    for key, value in dict.items(): 
        u = np.array(dict[key]['U1'])
        U.append(u)
        i = np.array(dict[key]['I'])
        I.append(i)
        t = np.array(dict[key]['t'])
        time.append(t)

    U_array = np.concatenate(U)
    I_array = np.concatenate(I)
    time_array = np.concatenate(time)
    scaled_time_array = time_array - time_array[0] 

    return U_array, scaled_time_array, I_array #U_array[start:end], scaled_time_array[start:end], I_array[start:end]


def plot_cycling(MJs): 
    fig, ax1 = plt.subplots(figsize=(6, 6))
    i = 1
    for idx in range(0, len(MJs)): 
        U, time, I = extract_data(MJs[idx])
        # Only plotting the cycle I am interested in (here: C/5 cycle)
        w = np.where(U == 3.0)
        start = 1614
        end = 5180
        U, time, I = U[start:end], time[start:end], I[start:end]
        ax1.plot(time, U, label = f'M1_02_'+str(idx+1))
        i += 1

    ax1.set_xlabel('t')
    ax1.set_ylabel('U', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.legend(loc='upper right')
    plt.title('C/5 cycling')
    return plt.show()
