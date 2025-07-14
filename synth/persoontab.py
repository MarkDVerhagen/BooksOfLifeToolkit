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

gbahh = pd.read_csv(os.path.join('synth', 'data', 'household_bus.csv'))

# Ensure only people present in household_bus are included
gbahh_rinpersoons = set(gbahh['rinpersoon'])

gbapersoon = gbahh.sort_values(by=['rinpersoon', 'DATUMAANVANGHH'], ascending=True).\
    groupby('rinpersoon').first()

# Filter gbapersoon to only those in household_bus
gbapersoon = gbapersoon[gbapersoon.index.isin(gbahh_rinpersoons)]

gbapersoon['age'] = gbapersoon['PLHH'].apply(assign_age)
# Ensure DATUMAANVANGHH is a string for slicing and int for comparison
gbapersoon['DATUMAANVANGHH'] = gbapersoon['DATUMAANVANGHH'].astype(str)

# Use integer comparison for date logic
gbapersoon['birthday'] = np.where(
    gbapersoon['DATUMAANVANGHH'].astype(int) > 19900101,
    gbapersoon['DATUMAANVANGHH'].str.slice(0, 4),
    1990 - gbapersoon['age']
)

## Simulate additional data
# Use integer comparison for GBAGEBOORTELAND assignment
gbapersoon['GBAGEBOORTELAND'] = np.where(
    gbapersoon['DATUMAANVANGHH'].astype(int) > 19900101,
    'NL',
    np.random.choice(['NL', 'France', 'US', 'Egypt'], p=[0.8, 0.15, 0.03, 0.02], size=len(gbapersoon))
)
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
    'GBAGEBOORTELANDNL'
    ]

gbapersoon.reset_index()[cols].to_csv(os.path.join('synth', 'data', 'persoon_tab.csv'),
                                      index=False)
