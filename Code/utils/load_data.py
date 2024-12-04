import numpy as np
from gamry_parser import GamryParser, Impedance
import pandas as pd

# at ca. 45% SoC (3.587 V)
# at 25 deg C

def get_exp_data(i, d): 

    '''
    Extracts the experimental data in the form 
    [z_list, freq, len(freq)] 
    
    '''

    z_list = []
    file = "/Users/synnemard/Desktop/lithium_ion/EIS_data/MJ1_02_EIS-SoC/MJ1_02_EIS-SoC_0"+str(i)+"/"+d+"EISGALV3V587.DTA"
    ca = Impedance(file)
    ca.load(filename=file)

    # extract EIS curve
    res = ca.get_curve_data().iloc[::-1]
    df_real = res['Zreal']
    df_imag= res['Zimag']
    df_freq = res['Freq']
    #df_name = res['Vdc']

    # Removing the points beneath the y-axis 
    real = df_real[df_imag <= 0]
    imag = df_imag[df_imag <= 0]
    freq = df_freq[df_imag <= 0]
    
    # Adding the impendances to the list 
    z_list.append(real)
    z_list.append(imag)
    return[z_list, freq, len(freq)] #, df_name]
