import pybamm as pb 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

def discharge_plotting_csv(parametre, path): 

    '''
    Reference 
    ---
    [1] Amund Raniseth. NTNU, Norway. 2024
    ---

    Function
    ---
    Plots the experimental discharge from a csv file, and also the PyBaMM simulated discharge. 
    ---

    '''
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


def discharge_plotting_txt(parametre, path): 

    '''
    Reference 
    ---
    [1] Amund Raniseth. NTNU, Norway. 2024
    ---
    
    Function
    ---
    Plots the experimental discharge from a csv file, and also the PyBaMM simulated discharge. 
    ---
    '''
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

    # Choosing which parameters to plot, the default is all parameters. 
    #output.plot()
    output_var = ["Current [A]", "Voltage [V]"]
    output.plot(output_variables = output_var)

    # Load the .txt file while skipping metadata rows
    exp_bench = pd.read_csv(
        path,
        delimiter="\t",          
        skiprows=7,              # Skips the first 7 rows
        names=["Rec", "Cycle P", "Cycle C", "Step", "Test Time", "Step Time", 
               "Capacity", "Energy", "Current", "Voltage", "MD", "ES", "DPT", "Time"
               ],                        
        usecols=["Test Time", "Current", "Voltage"])
    
    
    exp_bench["Test Time"] = exp_bench["Test Time"].astype(str)
    exp_bench["Test Time"] = pd.to_timedelta(exp_bench["Test Time"].str.strip(), errors='coerce').dt.total_seconds()
    exp_bench = exp_bench[exp_bench["Test Time"] < 11.8 * 3600]  # Time < 11.8 hours
    exp_bench = exp_bench[exp_bench["Test Time"] > 6.6 * 3600]   # Time > 6.6 hours
    exp_bench["Test Time"] = exp_bench["Test Time"] - exp_bench["Test Time"].iloc[0]

    # Plotting
    plt.plot(exp_bench["Test Time"] / 3600, exp_bench["Voltage"], label="Experiment")
    plt.plot(sim.solution['Time [s]'].entries/3600, sim.solution['Voltage [V]'].entries, label="Simulation")
    plt.xlabel("Time (hours)")
    plt.ylabel("Voltage (V)")
    plt.legend()
    plt.title("Voltage vs Time")
    return plt.show()


