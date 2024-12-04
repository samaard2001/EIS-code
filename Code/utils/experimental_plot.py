import matplotlib.pyplot as plt
from utils.load_data import get_exp_data
from utils.check_SOC import get_vdc

def plotting(i, d): 

    '''
    Plots the experimental Nyquist plot for a specified data set i. 

    Inputs: 
    i: data set number
    d: "d" is measured during discharge in the GITT-cycle. The default is d = "", 
    which means that the data is measured during charge in the GITT-cycle.
    '''

    # Creating Nyquist plot
    plt.figure(figsize=(6,6))
    plt.scatter(get_exp_data(i, d)[0][0], -get_exp_data(i, d)[0][1], color='red', label = str(round(get_vdc(i, d),2))+f' V')

    # Labeling the plot
    plt.xlabel('Real(Z) [Ω]')
    plt.ylabel('Imaginary(Z) [Ω]')
    plt.title('MJ1 cell degradation step '+str(i))
    plt.legend()
    plt.show()

def combined_plot(i):

    '''
    Plots the experimental Nyquist plot for a specified data set i, for both the data 
    measured during charge and during discharge in the GITT-cycle.  
    '''
    # Creating the figure for both the charged and discharged data
    plt.figure(figsize=(6, 6))

    z_list_charged = get_exp_data(i, "")[0]
    z_list_discharged = get_exp_data(i, "d")[0]

    # Plot 
    plt.scatter(z_list_charged[0], -z_list_charged[1], color='red', label='Charged: '+str(round(get_vdc(i, ""),2))+f' V')
    plt.scatter(z_list_discharged[0], -z_list_discharged[1], color='blue', label='Discharged: '+str(round(get_vdc(i, "d"),2))+f' V')

    # Adding labels and title
    plt.xlabel('Real(Z) [Ω]')
    plt.ylabel('Imaginary(Z) [Ω]')
    plt.title(f'MJ1 cell degradation step {i}')
    plt.legend()
    plt.show()