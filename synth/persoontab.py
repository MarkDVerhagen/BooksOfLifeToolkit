import pandas as pd
import os
import numpy as np
import random

def assign_age(value):
    value_list = ['single person', 'partner in couple without children',
                  'partner in couple with children', 'parent in single parent household']
    if value in value_list:
        return np.random.randint(20, 41)
    else:
        return np.random.randint(0, 11) 

gbahh = pd.read_csv(os.path.join('synth', 'data', 'householdbus.csv'))

gbapersoon = gbahh.sort_values(by=['rinpersoon', 'Start Date'], ascending=True).\
    groupby('rinpersoon').first()

gbapersoon['age'] = gbapersoon['Household Member place'].apply(assign_age)
gbapersoon['birth_date'] = np.where(gbapersoon['Start Date'] > '1990-01-01',
                                    gbapersoon['Start Date'].str.slice(0, 4),                                    
                                    1990 - gbapersoon['age'])

gbapersoon['birth_country'] = np.where(gbapersoon['Start Date'] > '1990-01-01',
                                       'NL', np.random.choice(['NL', 'France', 'US', 'Egypt'], p = [0.8, 0.15, 0.03, 0.02]))

gbapersoon[['birth_country', 'birth_date']].to_csv(os.path.join('synth', 'data', 'persoontab.csv'))
