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

gbahh = pd.read_csv(os.path.join('synth', 'data', 'raw', 'householdbus.csv'))

gbapersoon = gbahh.sort_values(by=['rinpersoon', 'DATE_STIRTHH'], ascending=True).\
    groupby('rinpersoon').first()

gbapersoon['age'] = gbapersoon['PLHH'].apply(assign_age)
gbapersoon['birthday'] = np.where(gbapersoon['DATE_STIRTHH'] > '1990-01-01',
                                  gbapersoon['DATE_STIRTHH'].str.slice(0, 4),                                    
                                  1990 - gbapersoon['age'])

## Simulate additional data
gbapersoon['GBAGEBOORTELAND'] = np.where(gbapersoon['DATE_STIRTHH'] > '1990-01-01',
                                         'NL', np.random.choice(['NL', 'France', 'US', 'Egypt'], p = [0.8, 0.15, 0.03, 0.02]))
gbapersoon['GBAGESLACHT'] = np.random.choice(['1', '2', '-'], size=len(gbapersoon), p=[0.49, 0.49, 0.02])
gbapersoon['GBAGEBOORTELANDMOEDER'] = np.random.choice(['NL', 'France', 'US', 'Egypt'], size=len(gbapersoon), p=[0.8, 0.15, 0.03, 0.02])
gbapersoon['GBAGEBOORTELANDVADER'] = np.random.choice(['NL', 'France', 'US', 'Egypt'], size=len(gbapersoon), p=[0.8, 0.15, 0.03, 0.02])
gbapersoon['GBAAANTALOUDERSBUITENLAND'] = gbapersoon.apply(lambda row: str(int(row['GBAGEBOORTELANDMOEDER'] != 'NL') + int(row['GBAGEBOORTELANDVADER'] != 'NL')), axis=1)
gbapersoon['GBAHERKOMSTGROEPERING'] = gbapersoon['GBAGEBOORTELAND'].apply(lambda x: 'Western' if x in ['NL', 'France', 'US'] else 'Non-Western')
gbapersoon['GBAGENERATIE'] = np.random.choice(['-', '0', '1', '2'], size=len(gbapersoon), p=[0.01, 0.3, 0.4, 0.29])
gbapersoon['GBAGEBOORTEJAAR'] = gbapersoon['birthday'].astype(int)
gbapersoon['GBAGESLACHTMOEDER'] = np.random.choice(['1', '2', '-'], size=len(gbapersoon), p=[0.01, 0.98, 0.01])
gbapersoon['GBAGESLACHTVADER'] = np.random.choice(['1', '2', '-'], size=len(gbapersoon), p=[0.98, 0.01, 0.01])
gbapersoon['GBAGEBOORTEJAARMOEDER'] = gbapersoon['GBAGEBOORTEJAAR'] - np.random.randint(20, 40, size=len(gbapersoon))
gbapersoon['GBAGEBOORTEJAARVADER'] = gbapersoon['GBAGEBOORTEJAAR'] - np.random.randint(20, 40, size=len(gbapersoon))
gbapersoon['GBAHERKOMSTLAND'] = gbapersoon['GBAGEBOORTELAND']
gbapersoon['GBAGEBOORTELANDNL'] = np.where(gbapersoon['GBAGEBOORTELAND'] == 'NL', '1', '0')

cols = [
    'rinpersoon',
    'GBAGEBOORTELAND',
    'GBAGESLACHT',
    'GBAGEBOORTELANDMOEDER',
    'GBAGEBOORTELANDVADER',
    'GBAAANTALOUDERSBUITENLAND',
    'GBAHERKOMSTGROEPERING',
    'GBAGENERATIE',
    'GBAGEBOORTEJAAR',
    'GBAGESLACHTMOEDER',
    'GBAGESLACHTVADER',
    'GBAGEBOORTEJAARMOEDER',
    'GBAGEBOORTEJAARVADER',
    'GBAHERKOMSTLAND',
    'GBAGEBOORTELANDNL',
    'birthday',
    ]

gbapersoon.reset_index()[cols].to_csv(os.path.join('synth', 'data', 'raw', 'persoontab.csv'),
                                      index=False)
