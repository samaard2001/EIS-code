import numpy as np 
import pybamm as pb 

def MJ1_ocp_tanh_SiC(sto):     
    x = sto     
    p = np.array([ 1.20912055e+00,  
                  5.62297420e+01, -1.11020020e-01, -2.53458213e-01, 4.92581391e+01,  
                  1.22046522e-02,  4.73538620e-02,  1.79631246e+01, 1.75283209e-01,  
                  1.88038929e-02,  3.03255334e+01,  4.66328034e-01])         
    return (             
        p[0] * pb.exp(-p[1] * x)             
        + p[2]             
        - p[3] * pb.tanh(p[4] * (x - p[5]))             
        - p[6] * pb.tanh(p[7] * (x - p[8]))            
          - p[9] * pb.tanh(p[10] * (x - p[11]))) 

def MJ1_ocp_tanh_NMC(sto):     
    x = sto     
    p = np.array([ 0.74041974,  4.39107343,  0.03434767, 18.16841489,  0.53463176,
                   17.68283504, 14.59709162,  0.28835348, 17.58474971, 14.69911523,  0.28845641])     
    return (             
        -p[0] * x             
        + p[1]             
        - p[2] * pb.tanh(p[3] * (x - p[4]))             
        - p[5] * pb.tanh(p[6] * (x - p[7]))             
        + p[8] * pb.tanh(p[9] * (x - p[10]))) 

EXCHANGE_CURRENT_DENSITY_SCALE = 2.8 
ELECTROLYTE_CONDUCTIVITY_SCALE = 1 

def graphite_exchange_current_density(c_e, c_s_surf, c_s_max, T):
    """     
    Exchange-current density for Butler-Volmer reactions between graphite and LiPF6 in     
    EC:DMC.   

    References    
    ----------     
    .. [1] Chang-Hui Chen, Ferran Brosa Planella, Kieran O’Regan, Dominika Gastol, W.    
    Dhammika Widanage, and Emma Kendrick. "Development of Experimental Techniques for    
    Parameterization of Multi-scale Lithium-ion Battery Models." Journal of the     
    Electrochemical Society 167 (2020): 080534.  

    Parameters     
    ----------     
    c_e : :class:`pybamm.Symbol`         
    Electrolyte concentration [mol.m-3]     
    c_s_surf : :class:`pybamm.Symbol`         
    Particle concentration [mol.m-3]     
    c_s_max : :class:`pybamm.Symbol`         
    Maximum particle concentration [mol.m-3]     
    T : :class:`pybamm.Symbol`         
    Temperature [K] 

    Returns     
    -------     
    :class:`pybamm.Symbol`         
    Exchange-current density [A.m-2]     
    """     

    m_ref = 6.48e-7  # (A/m2)(m3/mol)**1.5 - includes ref concentrations     
    E_r = 35000     
    arrhenius = pb.exp(E_r / pb.constants.R * (1 / 298.15 - 1 / T))     
    ex_cur_dens = m_ref * arrhenius * c_e**0.5 * c_s_surf**0.5 * (c_s_max - c_s_surf) * 0.5 * EXCHANGE_CURRENT_DENSITY_SCALE         
    return ex_cur_dens 

def nmc_exchange_current_density(c_e, c_s_surf, c_s_max, T):     
    """     
    Exchange-current density for Butler-Volmer reactions between NMC and LiPF6 in     
    EC:DMC.   
     
    References     
    ----------     
    .. [1] Chang-Hui Chen, Ferran Brosa Planella, Kieran O’Regan, Dominika Gastol, W.     
    Dhammika Widanage, and Emma Kendrick. "Development of Experimental Techniques for     
    Parameterization of Multi-scale Lithium-ion Battery Models." Journal of the     
    Electrochemical Society 167 (2020): 080534.     

    Parameters     
    ----------     
    c_e : :class:`pybamm.Symbol`         
    Electrolyte concentration [mol.m-3]     
    c_s_surf : :class:`pybamm.Symbol`         
    Particle concentration [mol.m-3]     
    c_s_max : :class:`pybamm.Symbol`        
    Maximum particle concentration [mol.m-3]     
    T : :class:`pybamm.Symbol`         
    Temperature [K] 

    Returns     
    -------     
    :class:`pybamm.Symbol`         
    Exchange-current density [A.m-2]     
    """     
    
    m_ref = 3.42e-6  # (A/m2)(m3/mol)**1.5 - includes ref concentrations     
    E_r = 17800     
    arrhenius = pb.exp(E_r / pb.constants.R * (1 / 298.15 - 1 / T))     
    ex_cur_dens = m_ref * arrhenius * c_e**0.5 * c_s_surf**0.5 * (c_s_max - c_s_surf) * 0.5 * EXCHANGE_CURRENT_DENSITY_SCALE     
    return ex_cur_dens 

def electrolyte_conductivity(c_e, T):     
    """     
    Conductivity of LiPF6 in EC:EMC (3:7) as a function of ion concentration. The data     
    comes from [1]. 

    References     
    ----------     
    .. [1] A. Nyman, M. Behm, and G. Lindbergh, "Electrochemical characterisation and     
    modelling of the mass transport phenomena in LiPF6-EC-EMC electrolyte,"     
    Electrochim. Acta, vol. 53, no. 22, pp. 6356–6365, 2008.    

    Parameters    
    ----------     
    c_e: :class:`pybamm.Symbol`         
    Dimensional electrolyte concentration     
    T: :class:`pybamm.Symbol`         
    Dimensional temperature   

    Returns     
    -------     
    :class:`pybamm.Symbol`         
    Solid diffusivity     
    """     
    sigma_e = (         
        0.1297 * (c_e / 1000) * 3 - 2.51 * (c_e / 1000) * 1.5 + 3.329 * (c_e / 1000)     
        ) * ELECTROLYTE_CONDUCTIVITY_SCALE     # Nyman et al. (2008) does not provide temperature dependence     
    return sigma_e

known_params = {     
    # 'Cell cooling surface area [m2]': 0.065 * 2*3.14*(0.018/2) + 2*(3.14*(0.018/2)**2),     
    # 'Cell volume [m3]': (3.14*(0.018/2)**2) * 0.065,     
    'Electrode height [m]': 0.059, 
    'Electrode width [m]': 0.610*2, # Multiplying by two since the electrode has active material on both sides.     
    'Lower voltage cut-off [V]': 2.5,     
    'Upper voltage cut-off [V]': 4.5,     
    'Nominal cell capacity [A.h]': 3.5,     # 'Number of cells connected in series to make a battery': 1.0,     
    'Number of electrodes connected in parallel to make a cell': 1.0,     # From Table 3 in https://doi.org/10.1016/j.jpowsour.2018.11.043     
    'Maximum concentration in negative electrode [mol.m-3]': 34684.0,     
    'Negative particle radius [m]': 6.1e-06,     
    'Negative electrode porosity': 0.216,     
    'Negative electrode active material volume fraction': 0.694,     
    # 'Negative electrode Bruggeman coefficient (electrolyte)': 1.5,     
    # 'Negative electrode charge transfer coefficient': 0.5,     
    'Negative electrode conductivity [S.m-1]': 100.0,     
    'Negative electrode diffusivity [m2.s-1]': 5e-14,     
    'Negative electrode OCP [V]': MJ1_ocp_tanh_SiC,     
    'Maximum concentration in positive electrode [mol.m-3]': 50060.0,     
    'Positive particle radius [m]': 3.8e-06,     
    'Positive electrode porosity': 0.171,     
    'Positive electrode active material volume fraction': 0.745,   
    # 'Positive electrode Bruggeman coefficient (electrolyte)': 1.85,     
    # 'Positive electrode charge transfer coefficient': 0.5,     
    'Positive electrode conductivity [S.m-1]': 0.17,     
    'Positive electrode diffusivity [m2.s-1]': 5e-13,     
    'Positive electrode OCP [V]': MJ1_ocp_tanh_NMC,     
    'Separator porosity': 0.45,     # end of section 3 data         
    
    # From Table A-9 and A-10 in https://doi.org/10.1016/j.jpowsour.2018.11.043     
    'Negative current collector conductivity [S.m-1]': 5.9e7/(1+3.383e-3 * (298.15-293.15)),      
    'Negative current collector thickness [m]': 11e-06,     
    'Negative current collector density [kg.m-3]': 8950.0,     
    'Negative current collector specific heat capacity [J.kg-1.K-1]': 385.0,     
    'Negative current collector thermal conductivity [W.m-1.K-1]': 398.0,     
    'Negative electrode density [kg.m-3]': 2242.0,     
    'Negative electrode specific heat capacity [J.kg-1.K-1]': 867.0,     
    'Negative electrode thermal conductivity [W.m-1.K-1]': 1.04,     
    'Negative electrode thickness [m]': 86.7e-6, # 86.7 in Sturm 2019, 85um in Heenan2020, 170um in NASA     
    'Negative electrode exchange-current density [A.m-2]': graphite_exchange_current_density,     
    'Positive current collector conductivity [S.m-1]': 3.78e7/(1+4.290e-3 * (298.15-293.15)),     
    'Positive current collector density [kg.m-3]': 2710.0,     
    'Positive current collector specific heat capacity [J.kg-1.K-1]': 903.0,     
    'Positive current collector thermal conductivity [W.m-1.K-1]': 238.0,     
    'Positive current collector thickness [m]': 17.3e-06,     
    'Positive electrode density [kg.m-3]': 4870.0,     
    'Positive electrode specific heat capacity [J.kg-1.K-1]': 840.1,     
    'Positive electrode thermal conductivity [W.m-1.K-1]': 1.58,     
    'Positive electrode thickness [m]': 66.2e-6, #66.2um in Sturm2019, 72.5um in Heenan2020, 160um in NASA     
    'Positive electrode exchange-current density [A.m-2]': nmc_exchange_current_density,     
    'Separator density [kg.m-3]': 1009.0,     
    'Separator specific heat capacity [J.kg-1.K-1]': 1978.2,     
    'Separator thermal conductivity [W.m-1.K-1]': 0.33,     
    'Separator thickness [m]': 12e-06,     # end of table data
    'EC initial concentration in electrolyte [mol.m-3]': 1000,     
    } 

# This is just experimenting with new values
experimental_params = {     
    'Positive electrode diffusivity [m2.s-1]': 5e-13*0.025,     
    'Negative electrode diffusivity [m2.s-1]': 5e-14*0.3,     
    'Negative electrode Bruggeman coefficient (electrolyte)': 2,     
    'Positive electrode Bruggeman coefficient (electrolyte)': 2.1,  }

def params_2(): 
   # Use default parameters from the Chen2020 publication
   params = pb.ParameterValues("Chen2020")

   # Overwrite parameters with our own
   for parameter, value in known_params.items():
       try:
           if params[parameter] != value: # Check if the parameter exists in 'params' and has a different value
               params[parameter] = value # Update 'params' with the new value from 'known_params'
       except KeyError as e: # This block handles the case where the 'parameter' is not in 'params'
           print(f"Parameter {parameter} not part of default. Skipping.")
   return params