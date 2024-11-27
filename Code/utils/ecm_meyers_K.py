import numpy as np
from utils.parameters import params 
params = params()
from utils.convertion import list_to_dict
from utils.convertion import dict_to_list
from utils.potential_gradient import _dU_dc_anode

# Finding the potential gradiient from the stoichiometry 
params.set_initial_stoichiometries(0.45) # Setting SOC, this changes the initial concentrations
c_n = params['Initial concentration in negative electrode [mol.m-3]'] 
_dU_dc_a = _dU_dc_anode(c_n)

# Parameters for calculation of constants parameters below 
c_e = params['EC initial concentration in electrolyte [mol.m-3]']
T = 298 #K
F = 96485 #C/mol 
R = 8.314 #J/mol*K
n = 1 
e_a = 1 - params['Negative electrode porosity']
area_electrode = params['Electrode height [m]']*params['Electrode width [m]'] #[m^2]

# Constant parameters
Rs_a = params['Negative particle radius [m]']
L_a = params['Negative electrode thickness [m]'] 
sigma_a = params['Negative electrode conductivity [S.m-1]'] 
epsilon_a = e_a # volume fraction anode
K_a = (params['Electrolyte conductivity [S.m-1]'](c_e, T)*epsilon_a)/params['Negative electrode Bruggeman coefficient (electrolyte)']

# Meyers component parameters
a_meyers_K = {
    "Rel": 0.00192, # to move the plot
    "K": 0.05, # conductivity, [S.m-1]
    "R1": 0.005,  # motstand, [ohm.m^2]
    "R2": 0.005, 
    "Q1": 0.7,  # kapasitans
    "Q2": 0.9, 
    "alpha_q1": 0.75,
    "alpha_q2": 0.8,
    "Ds": 4.1e-15,     # diffusjonskoeffisient [m^2.s^-1]
    "alpha": 0.93, #ikke-ideell diffusjon
    "a": 428947,  # overflateareal porer/volum electrode [m^-1]
    }

def R_part(Ds): 
    R_part = _dU_dc_a*(Rs_a/(F*Ds))
    return R_part 

def Y_s(omega, Ds, alpha):
    omega_s = (omega*Rs_a**2)/Ds**alpha
    Y_s = (np.sqrt(1j*omega_s) - np.tanh(np.sqrt(1j*omega_s)))/np.tanh(np.sqrt(1j*omega_s))
    return Y_s

def Y_particle(omega, R1, R2, Q1, Q2, alpha_q1, alpha_q2, R_part, Y_s): 
    Y = 1/((R1 + R_part/Y_s)/(1 + (1j*omega)**alpha_q1*Q1*(R1 + R_part/Y_s)) + R2/(1 + (1j*omega)**alpha_q2*Q2*R2))
    return Y

def v(a, Y, K): 
    v = L_a/ (((K*sigma_a)/(K + sigma_a))**0.5*((a*Y))**(-0.5))
    return v

# Function to calculate Z 
def calc_meyers_K_Z(comp, frequencies):
    # Update param dictionary from the flat parameter list (comp), where comp is updated values
    param = list_to_dict(a_meyers_K, comp) 
    ang_freq = 2 * np.pi * frequencies

    Rp = R_part(param['Ds'])
    Ys = Y_s(ang_freq, param['Ds'], param['alpha'])
    Y = Y_particle(ang_freq, param['R1'], param['R2'], param['Q1'], param['Q2'], param['alpha_q1'], param['alpha_q2'], Rp, Ys)
    v_calc = v(param['a'], Y, param['K'])

    # The total impedance: 
    Z = (param['Rel'] + (L_a/(param['K']+sigma_a))*(1 + (2 + (sigma_a/param['K'] + param['K']/sigma_a)*np.cosh(v_calc))/(v_calc*np.sinh(v_calc))))/area_electrode

    return Z