import pybamm as pb 
import pybammeis 
import numpy as np
from utils.load_data import get_exp_data

def calc_pybamm_Z(i, parametre, Rs): 
    '''
    Function to calculate the impedance Z from the PyBaMM parameters. 
    Inputs: 
    i: data set number
    parametre: parameter list
    Rs: ohmic (real) resistance
    '''
    # Defining the frequency range. Here, the same frequency range as 
    # the experimental frequency range for data set i is utilized. 
    freq = np.array(get_exp_data(i, "")[1])

    # Utilizing the Doyle-Fuller-Newman (DFN) model.
    # Adding the option 'surface form': 'differential' so that the 
    # double-layer capacitance is calculated. 
    model = pb.lithium_ion.DFN(options={"surface form": "differential"})

    # Generating an Electrochemical Impedance Spectroscopy (EIS) model, 
    # with chosen parameters called 'parametre'.
    eis_sim_func = pybammeis.EISSimulation(model, parameter_values=parametre)

    # Solving the simulation with the freequency rangge and the 
    # numeric method called 'prebicgstab'. 
    sim_f_func = eis_sim_func.solve(freq, method = "prebicgstab")
    
    # Returing the real impedance with an additional ohmic resistance, 
    # and an imaginary resistance. 
    return (sim_f_func.real + Rs) + sim_f_func.imag*1j


