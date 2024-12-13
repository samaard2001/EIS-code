from utils.geometry_params import R, T, n, F

def R_ct(i_0): 
    '''
    
    Finds the charge transfer resistance R_ct from exchange current density. 
    Assumption: 
    - linear, symmetric Butler-Volmer equation 

    '''
    return (R*T)/(n*F*i_0).__dict__['_value'] # [ohm.m^2]
