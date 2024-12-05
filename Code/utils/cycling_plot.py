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

    return U_array, scaled_time_array, I_array 

def find_index(list, value, tolerance): 
    # Find the index where the time is approximately equal to the target value
    indices = np.where(np.abs(list - value) < tolerance)[0]
    if indices.size > 0:
       return indices[0]
    else:
       return(print(f"No index found where time is approximately {value}."))

def plot_cycling(MJs): 
    fig, ax1 = plt.subplots(figsize=(6, 6))
    Us = []
    Is = []
    for idx in range(0, len(MJs)): 
        U, time, I = extract_data(MJs[idx])

        start = find_index(time, 52000, 10)
        U, time, I = U[start:], time[start:], I[start:]

        Us.append(U)
        Is.append(I)

        ax1.plot(time, U, label = f'M1_02_'+str(idx+1))
    
    c = find_index(Us[0], 3.587, 1e-3)

    # Calculate the change in resistance
    R_change = [(Us[i+1][c] - Us[i][c]) / (Is[i][c]) for i in range(len(Us)-1)]      

    ax1.set_xlabel('t')
    ax1.set_ylabel('U', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.legend(loc='upper right')
    plt.title('GITT cycling')
    plt.show()
    return print(f'The increase in resistance from data set 1 to 2, and 2 to 3 etc., is '+str(R_change))
