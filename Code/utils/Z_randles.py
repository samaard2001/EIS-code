from utils.convertion import dict_to_list, list_to_dict
import numpy as np

# Randles components parameters 
a_randles = {
    "R_el": 0.026455095283510706,  # Electrolyte resistance (Ohms)
    "L": 5.534820787666664e-07,    # Inductance (H)
    
    #Cathode? 
    "R_ct1": 0.0055426231465975665,  
    "Q1" : 0.6755099612832921, 
    "alpha1": 0.6624587164477784, 
    "A1": 0.0010503007445281985,     
    "a_w1": 0.5722885441839765, 

    #Anode? 
    "R_ct2": 0.005384825939881047,  
    "Q2" : 2.339974970415867, 
    "alpha2": 0.8629910852751331, 
    }

# Define non-ideal Warburg impedance
def wni_imp(omega, A, a_w): 
    return A/(1j*omega)**a_w

# CPE for non-ideal behaviour
def cpe_imp(omega, Q, alpha): 
    return 1/(Q*(1j*omega)**alpha)

# Define Inductance impedance
def i_imp(omega, L): 
    return 1j*omega*L

# Function to calculate Z 
def calc_randles_Z(comp, frequencies):
    '''
    Function to calculate the impedance Z from the ECM component parameters. 
    
    '''
    # Update a_randles dictionary from the flat parameter list (comp)
    elem_up = list_to_dict(a_randles, comp)
    ang_freq = 2 * np.pi * frequencies

    Z_W1 = wni_imp(ang_freq, elem_up["A1"], elem_up["a_w1"])
    Z_cdl1 = cpe_imp(ang_freq, elem_up["Q1"], elem_up["alpha1"])
    Z_L = i_imp(ang_freq, elem_up["L"])
    Z_cdl2 = cpe_imp(ang_freq, elem_up["Q2"], elem_up["alpha2"])

    # 2 
    Z1 =  1/(1/(elem_up["R_ct1"] + Z_W1) + 1/Z_cdl1)
    Z2 =  1/(1/(elem_up["R_ct2"]) + 1/Z_cdl2)
    Z = Z_L + elem_up["R_el"] + Z1 + Z2

    return Z