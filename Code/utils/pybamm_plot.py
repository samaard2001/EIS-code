import numpy as np
import pybammeis
import pybamm
import matplotlib.pyplot as plt 
from utils.load_data import get_exp_data
from utils.check_SOC import get_vdc

def pybamm_plotting(i, parametre): 
    frequencies = np.array(get_exp_data(i, "")[1])
    model = pybamm.lithium_ion.DFN(options={"surface form": "differential"})
    eis_sim_func = pybammeis.EISSimulation(model, parameter_values=parametre)
    sim_f_func = eis_sim_func.solve(frequencies, method = "prebicgstab")

    fig, ax = plt.subplots(figsize=(4, 4)) 
    pybammeis.nyquist_plot(sim_f_func, ax=ax, linestyle="-", label = f'Simulation', alpha=0.7)
    ax.scatter(np.array(get_exp_data(i, "")[0][0]), -np.array(get_exp_data(i, "")[0][1]), color = 'red', label=f"Experimental "+str(np.round(get_vdc(1, ""),3))+" V")
    ax.set_xlim(0, 0.083)
    ax.set_ylim(0, 0.04)
    plt.legend()
    plt.title('MJ1_02 cell')
    return plt.show()