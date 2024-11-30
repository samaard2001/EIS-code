import numpy as np
from utils.parameters import params
params = params()

c_n_max = params["Maximum concentration in negative electrode [mol.m-3]"]
c_n_s_max = c_n_max 
c_p_max = params["Maximum concentration in positive electrode [mol.m-3]"]
c_p_s_max = c_p_max

params.set_initial_stoichiometries(0.45) # Setting SOC, this changes the initial concentrations
c_n = params['Initial concentration in negative electrode [mol.m-3]'] 
c_n_s = c_n # for the surface of the particle
c_p = params['Initial concentration in positive electrode [mol.m-3]'] 
c_p_s = c_p

def sech_2(z): 
    return 1/np.cosh(z)**2

def _dU_dc_anode(c): 
    x = c/c_n_max
    # Har satt in for x i uttrykket for potensial lenger oppe og derivert med hensyn på c
    p = np.array([ 1.20912055e+00,  5.62297420e+01, -1.11020020e-01, -2.53458213e-01, 4.92581391e+01,  1.22046522e-02,  4.73538620e-02,  1.79631246e+01, 1.75283209e-01,  1.88038929e-02,  3.03255334e+01,  4.66328034e-01])
    dU_dc = -(p[6]*p[7]*sech_2(p[7]*(c/c_n_max-p[8])))/c_n_max - (p[3]*p[4]*sech_2(p[4]*(c/c_n_max-p[5])))/c_n_max - (p[9]*p[10]*sech_2(p[10]*(c/c_n_max-p[11])))/c_n_max - (p[0]*p[1]*np.exp(-p[1]*c/c_n_max))/c_n_max
    return -dU_dc # [V*m^3/mol]


def _dU_dc_cathode(c): 
    x = c/c_p_max
    # Har satt in for x i uttrykket for potensial lenger oppe og derivert med hensyn på c
    p = np.array([ 0.74041974,  4.39107343,  0.03434767, 18.16841489,  0.53463176, 17.68283504, 14.59709162,  0.28835348, 17.58474971, 14.69911523,  0.28845641])
    dU_dc = -(p[5]*p[6]*sech_2(p[6]*(c/c_p_max-p[7])))/c_p_max - (p[2]*p[3]*sech_2(p[3]*(c/c_p_max-p[4])))/c_p_max + (p[9]*p[8]*sech_2(p[9]*(c/c_p_max-p[10])))/c_p_max - p[0]
    return -dU_dc # [V*m^3/mol]
