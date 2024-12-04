import pandas as pd
import numpy as np
from utils.load_data import get_exp_data

def get_vdc(i, d): 
    ''''
    Takes in an experimental EIS data set and checks what the average potential is 
    (since the potential should be kept relatively constant). 
    The average potential should correspond to 3.587 V for a 45% SOC for example.

    Inputs: 
    i: data set number
    d: measured during discharge in the GITT-cycle. The default is d = "", 
    which means that the data is measured during charge in the GITT-cycle.

    '''
    length = get_exp_data(i, d)[2]
    file = "/Users/synnemard/Desktop/lithium_ion/EIS_data/MJ1_01_EIS-SoC_01-05/MJ1_01_EIS-SoC_0"+str(i)+"/"+d+"EISGALV3V587.DTA"
    df = pd.read_csv(file, delimiter='\t', skiprows=[i for i in range(0, 60)], encoding='ISO-8859-1')

    df_vdc = df['Vdc'][::-1]
    vdc = df_vdc[:length+1]
    v_list = np.array(vdc)

    sum = 0 
    for i in v_list: 
        sum += float(i) 
    v_avg = sum/len(v_list)

    return v_avg 