import pandas as pd
import numpy as np
import os
from params import synth_params
import datetime

medical_events = {'sprained ankle': [0, 0.15, 0.1, 0.1, 0.1, 0.1, 0.05],
                  'surgery': [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],}
years = list(
    range(synth_params['start_year'], (synth_params['start_year'] + synth_params['time_periods']))
)

persons = pd.read_csv(os.path.join('synth', 'data', 'persoontab.csv')).reset_index()\
    [['rinpersoon', 'birth_date']]

year = 1990

vektistab = pd.DataFrame()

for year in years:
    persons['age_index'] = round((year - persons['birth_date']) / 10)
    persons.loc[persons['age_index'] <= 0, 'age_index'] = 0
    
    def index_list(row, outcome='sprained ankle'):
        return medical_events[outcome][int(row['age_index'])]
    
    persons['ankle_prob'] = persons.apply(index_list, axis=1)
    persons['surgery_prob'] = persons.apply(index_list, args=('surgery',), 
                                            axis=1)
    def generate_binary(probability):
        return np.random.choice([0, 1], p=[1 - probability, probability])
    
    
    persons['sprained_ankle'] = persons['ankle_prob'].apply(generate_binary)
    persons['surgery'] = persons['surgery_prob'].apply(generate_binary)
    activities = pd.concat([persons[['rinpersoon', 'sprained_ankle']],
                            persons[['rinpersoon', 'surgery']]])
    activities = activities.loc[(activities['sprained_ankle'] == 1) | (activities['surgery'] == 1)]
    activities['activity'] = np.where(activities['sprained_ankle'] == 1, 'sprained_ankle', 'surgery')
    activities = activities[['rinpersoon', 'activity']]
    activities['date'] = activities['rinpersoon'].apply(lambda l: datetime.datetime(year, round(np.random.uniform(1, 12)), 1))
    vektistab = pd.concat([vektistab, activities])

vektistab.to_csv(os.path.join('synth', 'data', 'vektistab.csv'))