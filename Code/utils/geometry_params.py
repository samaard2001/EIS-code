from utils.parameters_2 import params_2 
params = params_2()

F = 96485 #C/mol 
R = 8.314 #J/mol*K
n = 1 
T = 298 # K

volume_anode = params['Electrode height [m]']*params['Electrode width [m]']*params['Negative electrode thickness [m]'] # [m^3]
volume_cathode = params['Electrode height [m]']*params['Electrode width [m]']*params['Positive electrode thickness [m]'] # [m^3]
area_electrode = params['Electrode height [m]']*params['Electrode width [m]'] #[m^2]

r_a = params['Negative particle radius [m]']
r_c = params['Positive particle radius [m]']
e_a = 1 - params['Negative electrode porosity']
e_c = 1 - params['Positive electrode porosity']

c_n_max = params["Maximum concentration in negative electrode [mol.m-3]"]
c_n_s_max = c_n_max 
c_p_max = params["Maximum concentration in positive electrode [mol.m-3]"]
c_p_s_max = c_p_max
c_e = params['EC initial concentration in electrolyte [mol.m-3]']
 
params.set_initial_stoichiometries(0.45) # Setting SOC, this changes the initial concentrations
c_n = params['Initial concentration in negative electrode [mol.m-3]'] 
c_n_s = c_n # for the surface of the particle
c_p = params['Initial concentration in positive electrode [mol.m-3]'] 
c_p_s = c_p

i_0_a = params['Negative electrode exchange-current density [A.m-2]'](c_e, c_n_s, c_n_s_max, T)
i_0_c = params['Positive electrode exchange-current density [A.m-2]'](c_e, c_p_s, c_p_s_max, T)

