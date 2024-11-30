import numpy as np 
from utils.geometry_params import e_a, volume_anode, r_a

N = e_a*volume_anode/((4*np.pi/3)*r_a**3)

def a(V_electrode, e): 
    V_particle = (4*np.pi/3)*r_a**3
    V_active = e*V_electrode 
    # Number of particles
    N = V_active/V_particle 
    # Surface area of particle 
    A_particle = 4*np.pi*r_a**2
    # Total surface area of particles
    A_total = N*A_particle # so that A_total = (3*e)/r_particle
    return A_total/V_electrode # [m^-1]