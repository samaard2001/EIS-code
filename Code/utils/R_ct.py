from utils.geometry_params import R, T, n, F

def R_ct(i_0): 
    return (R*T)/(n*F*i_0).__dict__['_value'] # [ohm.m^2]

#R1_a = R_ct(i_0_a).__dict__['_value']
#R1_c = R_ct(i_0_c).__dict__['_value']