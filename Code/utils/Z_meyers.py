import numpy as np
from utils.known_parameters import params_func 
params = params_func()
from utils.convertion import list_to_dict, dict_to_list
from utils.geometry_params import R, T, n, F, e_a, c_n, area_electrode, c_e  
from utils.potential_gradient import _dU_dc_anode
_dU_dc_a = _dU_dc_anode(c_n)


# Constant parameters
Rs_a = params['Negative particle radius [m]']
L_a = params['Negative electrode thickness [m]'] 
sigma_a = params['Negative electrode conductivity [S.m-1]']*e_a
e_s = params['Negative electrode porosity']
K_a = (params['Electrolyte conductivity [S.m-1]'](c_e, T)*e_s)/params['Negative electrode Bruggeman coefficient (electrolyte)']

# Meyers component parameters
a_meyers = {
    "Rel": 0.0019, 
    "R1": 0.011,  
    "R2": 0.008, 
    "Q1": 0.8,  
    "Q2": 0.8, 
    "alpha_q1": 0.70,
    "alpha_q2": 0.8,
    "Ds": 4.1e-15,     
    "a": 428947,  
    }

def R_part(Ds): 
    R_part = _dU_dc_a*(Rs_a/(F*Ds))
    return R_part 

def Y_s(omega, Ds):
    omega_s = (omega*Rs_a**2)/(Ds)
    Y_s = (np.sqrt(1j*omega_s) - np.tanh(np.sqrt(1j*omega_s)))/np.tanh(np.sqrt(1j*omega_s))
    return Y_s

def Y_particle(omega, R1, R2, Q1, Q2, alpha_q1, alpha_q2, R_part, Y_s): 
    Y = 1/((R1 + R_part/Y_s)/(1 + (1j*omega)**alpha_q1*Q1*(R1 + R_part/Y_s)) + R2/(1 + (1j*omega)**alpha_q2*Q2*R2))
    return Y

def v(a, Y): 
    v = L_a/ (((K_a*sigma_a)/(K_a + sigma_a))**0.5*((a*Y))**(-0.5))
    return v


def calc_meyers_Z(comp, frequencies):
    '''
    Function to calculate the impedance Z from the Meyers component parameters. 
    
    '''
    # Update param dictionary from the flat parameter list (comp), where comp is updated values
    param = list_to_dict(a_meyers, comp) 
    ang_freq = 2 * np.pi * frequencies

    Rp = R_part(param['Ds'])
    Ys = Y_s(ang_freq, param['Ds'])
    Y = Y_particle(ang_freq, param['R1'], param['R2'], param['Q1'], param['Q2'], param['alpha_q1'], param['alpha_q2'], Rp, Ys)
    v_calc = v(param['a'], Y)

    # The total impedance: 
    Z = (param['Rel'] + (L_a/(K_a+sigma_a))*(1 + (2 + (sigma_a/K_a + K_a/sigma_a)*np.cosh(v_calc))/(v_calc*np.sinh(v_calc))))/area_electrode
    
    return Z
