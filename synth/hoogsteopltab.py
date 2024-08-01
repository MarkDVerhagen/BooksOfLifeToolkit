import numpy as np
import os
import pandas as pd
import random
import json
from params import synth_params

# Setup starting data
hoogste_opl = pd.read_csv('./synth/data/raw/persoon_tab.csv')[['rinpersoon', 'GBAGEBOORTEJAAR']]
hoogste_opl = hoogste_opl.assign(year = 2010)
hoogste_opl['education_level'] = [np.random.randint(1, 18) for i in range(hoogste_opl.shape[0])]
df = hoogste_opl
# Function to simulate employment status for T months
def simulate_education(df, T, education_prob = 0.1):
    for t in range(T):
        temp = df.loc[df['year'] == (2009 + t)]
        temp = temp.assign(age = 2009 + t - temp['GBAGEBOORTEJAAR'])
        
        temp['education_level'] = temp.apply(
            lambda x: x['education_level'] + 1 if (np.random.rand() <= education_prob) and x['age'] <= 30 else 
            x['education_level'], axis=1
        )
        temp['year'] = temp['year'] + 1
        
        df = pd.concat([df[['rinpersoon', 'year', 'education_level', 'GBAGEBOORTEJAAR']],
                        temp[['rinpersoon', 'year', 'education_level', 'GBAGEBOORTEJAAR']]])
        
    return df


results = simulate_education(hoogste_opl, T=10)

# Define function to generate OPLNRHB and OPLNRHG codes
def generate_codes():
    OPLNRHB = f"{random.randint(800000, 899999)}"
    OPLNRHG = f"{random.randint(100000, 199999)}"
    return OPLNRHB, OPLNRHG

# Generate OPLNRHB and OPLNRHG codes
results['OPLNRHB'], results['OPLNRHG'] = zip(*[generate_codes() for _ in range(len(results))])

# Assign Literal values for SOI classifications
results['OPLNIVSOI2016AGG4HBMETNIRWO'] = '-'
results['OPLNIVSOI2016AGG4HGMETNIRWO'] = '-'
results['RICHTdetailISCEDF2013HBmetNIRWO'] = '-'
results['RICHTdetailISCEDF2013HGmetNIRWO'] = '-'
results['OPLNIVSOI2021AGG4HBmetNIRWO'] = '-'
results['OPLNIVSOI2021AGG4HGmetNIRWO'] = '-'
results['RICHTSOI2021SCEDF2013HBNIRWO'] = '-'
results['RICHTSOI2021SCEDF2013HGNIRWO'] = '-'


results.to_csv(
    os.path.join('synth', 'data', 'raw', 'hoogsteopl_tab.csv'), index=False)
