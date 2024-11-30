import numpy as np
import matplotlib.pyplot as plt 
from utils.parameters_2 import params_2
params = params_2()
from utils.load_data import get_exp_data
from utils.check_SOC import get_vdc
from utils.convertion import list_to_dict, dict_to_list
from utils.geometry_params import T, R, F, n, c_e, c_n, volume_anode, area_electrode, i_0_a, e_a, r_a
from utils.potential_gradient import _dU_dc_anode
_dU_dc_a = _dU_dc_anode(c_n)
from utils.R_ct import R_ct
R1_a = R_ct(i_0_a)
from utils.pore_surface_area import a

# Meyers component parameters
a_meyers_initial = { 
    "R1": R1_a,  
    "C1": params['Negative electrode double-layer capacity [F.m-2]'],  
    "Rs": params['Negative particle radius [m]'], 
    "Ds": params['Negative electrode diffusivity [m2.s-1]'],     
    "a": a(volume_anode, e_a),  
    "L": params['Negative electrode thickness [m]'],  
    "K" : (params['Electrolyte conductivity [S.m-1]'](c_e, T)*e_a)/params['Negative electrode Bruggeman coefficient (electrolyte)'],  # ledningsevne elektrolytt [S.m^-1]
    "sigma": params['Negative electrode conductivity [S.m-1]'], 
    "ebsilon": e_a,     
    "-dU_dcs": _dU_dc_a, 
    }
ami = a_meyers_initial
print(ami)


def R_part(): 
    R_part = ami['-dU_dcs']*(ami['Rs']/(F*ami['Ds']))
    return R_part 

def Y_s(omega):
    omega_s = (omega*ami['Rs']**2)/ami['Ds']
    Y_s = (np.sqrt(1j*omega_s) - np.tanh(np.sqrt(1j*omega_s)))/np.tanh(np.sqrt(1j*omega_s))
    return Y_s

def Y_particle(omega, R_part, Y_s): 
    Y = 1/((ami['R1'] + R_part/Y_s)/(1 + (1j*omega)*ami['C1']*(ami['R1'] + R_part/Y_s)))
    return Y

def v(Y): 
    v = ami['L']/ (((ami['K']*ami['sigma'])/(ami['K'] + ami['sigma']))**0.5*((ami['a']*Y))**(-0.5))
    return v

# Function to calculate Z 
def calc_meyers_initial_Z(comp, frequencies):
    param = list_to_dict(a_meyers_initial, comp) 
    ang_freq = 2 * np.pi * frequencies

    Rp = R_part()
    Ys = Y_s(ang_freq)
    Y = Y_particle(ang_freq, Rp, Ys)
    v_calc = v(Y)

    # The total impedance: 
    Z = ((param['L']/(param['K']+param['sigma']))*(1 + (2 + (param['sigma']/param['K'] + param['K']/param['sigma'])*np.cosh(v_calc))/(v_calc*np.sinh(v_calc))))/area_electrode

    return Z

# Function for Nyquist plot
def plotting_meyers_initial(i): 
    frequencies = np.array(get_exp_data(i, "")[1])
    Z = calc_meyers_initial_Z(dict_to_list(a_meyers_initial), frequencies)

    fig, ax = plt.subplots(figsize=(6, 6)) 
    ax.scatter(np.array(get_exp_data(i, "")[0][0]), -np.array(get_exp_data(i, "")[0][1]), color = 'red', label=f"Experimental "+str(np.round(get_vdc(i, ""),3))+" V") 
    ax.scatter(Z.real, -Z.imag, label = f'Initial Meyers model', color = 'blue')
    plt.legend()
    plt.title("Comparing Meyers model with experimental") 
    plt.show() 