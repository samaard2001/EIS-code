import pybamm as pb 
import pybammeis 
import numpy as np
from utils.load_data import get_exp_data

def calc_pybamm_Z(i, parametre, Rel): 
    freq = np.array(get_exp_data(i, "")[1])

    model = pb.lithium_ion.DFN(options={"surface form": "differential"})
    eis_sim_func = pybammeis.EISSimulation(model, parameter_values=parametre)
    sim_f_func = eis_sim_func.solve(freq, method = "prebicgstab")
    return (sim_f_func.real + Rel) + sim_f_func.imag*1j


