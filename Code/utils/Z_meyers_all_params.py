import numpy as np
from utils.known_parameters import params_func
params = params_func()
from utils.convertion import list_to_dict
from utils.convertion import dict_to_list
from utils.geometry_params import R, T, n, F, e_a, c_n, area_electrode 
from utils.potential_gradient import _dU_dc_anode
_dU_dc_a = _dU_dc_anode(c_n)

eta = e_a/params['Negative electrode Bruggeman coefficient (electrolyte)']

# Meyers component parameters
a_meyers_all = {
    "Rel": 0.0242, # to move the plot
    "Rs": 6.1e-06, 
    "L": 8.67e-05,
    "sigma": 100.0, 
    "epsilon": 0.784, 
    "K": 0.05, # conductivity, [S.m-1]
    "R1": 0.0072,  # motstand, [ohm.m^2]
    "R2": 0.0072, 
    "Q1": 1,  # kapasitans
    "Q2": 1.2, 
    "alpha_q1": 0.75,
    "alpha_q2": 0.8,
    "Ds": 1.0e-16,     # diffusjonskoeffisient [m^2.s^-1]
    "eta": 0.9, #ikke-ideell diffusjon
    "a": 428947,  # overflateareal porer/volum electrode [m^-1]
    "I": 5.534820787666664e-07 
    }


def R_part(Ds, Rs): 
    R_part = _dU_dc_a*(Rs/(F*Ds))
    return R_part 

def Y_s(omega, Ds, Rs, eta):
    omega_s = (omega*Rs**2)/(Ds*eta)
    Y_s = (np.sqrt(1j*omega_s) - np.tanh(np.sqrt(1j*omega_s)))/np.tanh(np.sqrt(1j*omega_s))
    return Y_s

def Y_particle(omega, R1, R2, Q1, Q2, alpha_q1, alpha_q2, R_part, Y_s): 
    Y = 1/((R1 + R_part/Y_s)/(1 + (1j*omega)**alpha_q1*Q1*(R1 + R_part/Y_s)) + R2/(1 + (1j*omega)**alpha_q2*Q2*R2))
    return Y

def v(a, Y, K, sigma, L): 
    v = L/ (((K*sigma)/(K + sigma))**0.5*((a*Y))**(-0.5))
    return v

# Define Inductance impedance
def i_imp(omega, I): 
    return 1j*omega*I

# Function to calculate Z 
def calc_meyers_all_Z(comp, frequencies):
    # Update param dictionary from the flat parameter list (comp), where comp is updated values
    param = list_to_dict(a_meyers_all, comp) 
    ang_freq = 2 * np.pi * frequencies

    Rp = R_part(param['Ds'], param['Rs'])
    Ys = Y_s(ang_freq, param['Ds'], param['Rs'], param['eta'])
    Y = Y_particle(ang_freq, param['R1'], param['R2'], param['Q1'], param['Q2'], param['alpha_q1'], param['alpha_q2'], Rp, Ys)
    v_calc = v(param['a'], Y, param['K'], param['sigma'], param['L'])
    Z_L = i_imp(ang_freq, param["I"])

    # The total impedance: 
    Z =  Z_L + param['Rel'] + ((param['L']/(param['K']+param['sigma']))*(1 + (2 + (param['sigma']/param['K'] + param['K']/param['sigma'])*np.cosh(v_calc))/(v_calc*np.sinh(v_calc))))/area_electrode

    return Z