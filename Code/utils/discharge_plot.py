import pybamm as pb 
import pandas as pd 
import matplotlib.pyplot as plt 

def discharge_plotting(parametre, path): 
    model = pb.lithium_ion.DFN(options={"surface form": "differential"})
    # Define experiment
    experiment = pb.Experiment([
    ("Rest for 1 minutes"),
    ("Discharge at C/5 for 12 hours or until 3.0 V"),
    ])   

    # Simulate the experiment using the model with the updated parameter set
    sim = pb.Simulation(model,  parameter_values=parametre, experiment=experiment) # , 
    safe_solver = pb.CasadiSolver(mode="fast", return_solution_if_failed_early=True)
    output = sim.solve(solver=safe_solver, calc_esoh=False)
    output.plot()

    # Load experimental data & select relevant discharge
    exp_bench = pd.read_csv(path)
    #exp_bench = pd.read_csv("MJ1_01_01.csv")
    exp_bench["t"] = exp_bench["t"] - exp_bench["t"].iloc[0]
    exp_bench = exp_bench[exp_bench["t"] < 12*3600]
    exp_bench = exp_bench[exp_bench["t"] > 2*3600]
    exp_bench = exp_bench[exp_bench["I"]<0] # Remove charge cycle
    exp_bench["t"] = exp_bench["t"] - exp_bench["t"].iloc[0]

    # Plotting 
    plt.plot(exp_bench["t"]/3600, exp_bench["U1"], label="Experiment")
    plt.plot(sim.solution['Time [s]'].entries/3600, sim.solution['Voltage [V]'].entries, label="Simulation")
    plt.xlabel("Experiment time, h")
    plt.ylabel("Voltage, V")
    plt.legend()
    return plt.show()