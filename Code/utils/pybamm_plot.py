import numpy as np
import pybammeis
import pybamm
import matplotlib.pyplot as plt 
from utils.load_data import get_exp_data
from utils.check_SOC import get_vdc

# Changing state of charge SOC

def set_SOC(parametre, z): 

    ''''
    Setting state of charge SoC.
    '''
    x0, x100, y100, y0 = pybamm.lithium_ion.get_min_max_stoichiometries(parametre)
    x = x0 + z * (x100 - x0)
    y = y0 - z * (y0 - y100)
    c_n_max = parametre["Maximum concentration in negative electrode [mol.m-3]"]
    c_p_max = parametre["Maximum concentration in positive electrode [mol.m-3]"]

    return parametre.update({
        "Initial concentration in negative electrode [mol.m-3]": x * c_n_max,
        "Initial concentration in positive electrode [mol.m-3]": y * c_p_max,
        })


def nyquist_plot(data, Rel, ax=None, marker="o", linestyle="None", **kwargs):
    """
    Reference
    ---
    [1] Sulzer, V., Marquis, S. G., Timms, R., Robinson, M., & Chapman, S. J. (2021). 
    “Python Battery Mathematical Modelling (PyBaMM)”. Journal of Open Research Software,9 (1), 14.
    Url: https://github.com/pybamm-team/pybamm-eis/blob/922b68e8187149b73c190ec57cc727e448c3acd9/pybammeis/plotting.py#L5
    ---

    Adding an ohmic resistance called Rel to align the experimental and simulated plots. 
    """

    if isinstance(data, list):
        data = np.array(data)

    if ax is None:
        _, ax = plt.subplots()
        show = True
    else:
        show = False

    ax.plot(data.real + Rel, -data.imag, marker=marker, linestyle=linestyle, **kwargs)
    _, xmax = ax.get_xlim()
    _, ymax = ax.get_ylim()
    axmax = max(xmax, ymax)
    plt.axis([0, axmax, 0, axmax])
    plt.gca().set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$Z_\mathrm{Re}$ [Ohm]")
    ax.set_ylabel(r"$-Z_\mathrm{Im}$ [Ohm]")
    if show:
        plt.show()

    return ax

def pybamm_plotting(i, parametre, Rel, xlim, ylim): 
    '''
    Plotting PyBaMM simulation and comparing with experimental in Nyquist plot. 
    '''
    frequencies = np.array(get_exp_data(i, "")[1])
    model = pybamm.lithium_ion.DFN(options={"surface form": "differential"})
    eis_sim_func = pybammeis.EISSimulation(model, parameter_values=parametre)
    sim_f_func = eis_sim_func.solve(frequencies, method = "prebicgstab")
    fig, ax = plt.subplots(figsize=(4, 4)) 
    nyquist_plot(sim_f_func, Rel, ax=ax, linestyle="-", label = f'Simulation', alpha=0.7)
    ax.scatter(np.array(get_exp_data(i, "")[0][0]), -np.array(get_exp_data(i, "")[0][1]), color = 'red', label=f"Experimental "+str(np.round(get_vdc(1, ""),3))+" V")
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(ylim[0], ylim[1])
    plt.legend()
    plt.title('MJ1_02 cell')
    return plt.show()