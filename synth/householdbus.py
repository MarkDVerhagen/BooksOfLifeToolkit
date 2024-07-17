import os
from pathlib import Path
import random
from datetime import datetime, timedelta
from params import synth_params
import json
from copy import copy, deepcopy
import pandas as pd
import numpy as np
from datetime import datetime

# Load hashed set of individuals and households
with open(os.path.join('synth', 'hashed_ids_' + str(synth_params['N_hash']) + '.json'), 'r') as f:
    hash_set = json.load(f)

with open(os.path.join('synth', 'hashed_hh_ids_' + str(synth_params['N_hh_hash']) + '.json'), 'r') as f:
    household_hash_set = json.load(f)

place_descriptions = {
    1: 'child living at home',
    2: 'single person',
    3: 'partner in couple without children',
    4: 'partner in couple with children',
    5: 'parent in single parent household',
}

child_born_map = {
    'child living at home': 'child living at home',
    'single person': 'parent in single parent household',
    'partner in couple without children': 'partner in couple with children',
    'partner in couple with children': 'partner in couple with children',
    'parent in single parent household': 'parent in single parent household',
}

adult_places = ['single person', 'partner in couple without children',
                'partner in couple with children', 'parent in single parent household']

class HouseholdMember:
    def __init__(self, id, place):
        self.id = id
        self.place = place

class Household:
    def __init__(self, id, members=[], empty=False):
        self.id = id
        self.members = members
        self.spells = []
        self.household_type = self.draw_household_type()
        self.generate_members_based_on_type()
    
    def draw_household_type(self):
        types = [
            'single person household',
            'couple without children',
            'couple with children',
            'single parent household',
        ]
        return random.choice(types)
    
    def generate_members_based_on_type(self):
        type_to_places = {
            'single person household': [2],
            'couple without children': [3, 3],
            'couple with children': [4, 4] + [1] * random.randint(1, 3),
            'single parent household': [5] + [1] * random.randint(1, 3),
        }

        places = type_to_places.get(self.household_type)
        self.members = [
            HouseholdMember(id=hash_set.pop(), place=place_descriptions[place]) for i, place in
            enumerate(places)]

def generate_initial_households(N):
    households = []
    for n in range(N):
        household = Household(household_hash_set.pop())
        household.spells = [datetime(1990, 1, 1), datetime(1991, 1, 1)]

        households.append(household)
    return households

def assign_household_type(hh):
    
    if len(hh.members) == 1:
        return 'single person household'
    if any([h.place == 'parent in single parent household' for h in hh.members]):
        return 'single parent household'
    if any([h.place == 'child living at home' for h in hh.members]):
        return 'couple with children'
    else:
        return 'couple without children'

def simulate_movement(households_input):
    events = ['breakup',  # household dissolves into two
              'child_born',  # household is retained and expanded
              'couple_formed',  # new household is generated
              'nothing']  # household is retained
    
    probs = {'single person household': [0, 0.05, 0.65, 0.3],
             'couple without children': [0.4, 0.25, 0, 0.35],
             'couple with children': [0.2, 0.05, 0, 0.75],
             'single parent household': [0, 0.01, 0.5, 0.49]}
    candidate_couple = []
    households_output = []
    
    for i in range(len(households_input)):
        hh = deepcopy(households_input[i])
        event_probs = probs[hh.household_type]
        event = np.random.choice(events, p=event_probs)
        
        if event == 'nothing':
            hh.spells = [hh.spells[-1], datetime(hh.spells[-1].year + 1, 1, 1)]
            households_output.append(hh)
        if event == 'child_born':
            hh.spells = [hh.spells[-1], datetime(hh.spells[-1].year + 1, 1, 1)]
            hh.members.append(HouseholdMember(id = hash_set.pop(),
                                              place = place_descriptions[1]))
            for m in hh.members:
                m.place = child_born_map[m.place]
            
            hh.household_type = assign_household_type(hh)
            households_output.append(hh)
        if event == 'breakup':
            children = [h for h in hh.members if h.place == 'child living at home']
            parents = [h for h in hh.members if h.place != 'child living at home']
            
            old_hh = deepcopy(hh)
            old_hh.members = [parents[0]] + children
            
            if children:
                old_hh.members[0].place = 'parent in single parent household'
            else:
                old_hh.members[0].place = 'single person'

            old_hh.spells = [hh.spells[-1], datetime(hh.spells[-1].year + 1, 1, 1)]
            old_hh.household_type = assign_household_type(old_hh)

            new_hh = deepcopy(hh)
            new_hh.id = household_hash_set.pop()
            new_hh.members = [parents[1]]
            new_hh.household_type = 'single person household'
            new_hh.members[0].place = 'single person'
            
            new_hh.spells = [hh.spells[-1], datetime(hh.spells[-1].year + 1, 1, 1)]
            
            households_output.append(new_hh)
            households_output.append(old_hh)

        if event == 'couple_formed':
            if not candidate_couple:
                candidate_couple = [hh]
            else:
                new_hh = deepcopy(candidate_couple.pop())
                new_hh.members = new_hh.members +\
                    hh.members
                if (len(new_hh.members) > 2):
                    for m in new_hh.members:
                        if m.place in adult_places:
                            m.place = 'partner in couple with children'
                        else:
                            m.place = 'child living at home'
                if (len(new_hh.members) == 2):
                    for m in new_hh.members:
                        m.place = 'partner in couple without children'
                new_hh.spells = [new_hh.spells[-1], datetime(new_hh.spells[-1].year + 1, 1, 1)]
                new_hh.household_type = assign_household_type(new_hh)
                households_output.append(new_hh)
            
    return households_output

def collect_data_for_dataframe_separate_rows(households):
    data = pd.DataFrame()
    for household in households:
        household_size = len(household.members)
        
        hh_dict = {
                    'HOUSEKEEPING_NR': household.id,
                    'TYPHH': household.household_type,
                    'rinpersoon': [h.id for h in household.members],
                    'PLHH': [h.place for h in household.members],
                    'REFPERSOONHH': round(np.random.choice([0, 1])),
                    'NUMBERPERSHH': len(household.members),
                    'DATE_STIRTHH': household.spells[0],
                    'DATUMEINDEHH': household.spells[1],  # Handling ongoing spels
                    'AANTALOVHH': len([h.place for h in household.members if h.place != 'child living at home']),
                    'AANTALKINDHH': len([h.place for h in household.members if h.place == 'child living at home']),
                }
        
        normalized_hh_dict = {k: [v] * household_size if not isinstance(v, list)
                              else v for k, v in hh_dict.items()}

        data = pd.concat([data, pd.DataFrame(normalized_hh_dict)])
    return data

def describe_hh(hh):
    print(hh.household_type)
    print([h.place for h in hh.members])

# Get initialization parameters
N_households = synth_params['N_hh']
time_periods = synth_params['time_periods']

# Initialize households
start_households = generate_initial_households(N_households)

# Simulate time_periods ahead
t = 1
# Initialize list with households per time period
households_list = [start_households]

while t < time_periods:
    households_list.append(simulate_movement(households_list[-1]))
    t += 1

hh_df = pd.concat([collect_data_for_dataframe_separate_rows(hh) for hh in households_list])

# Draw additional random values to align with documentation
def process_household(df):
    df['BIRTHEDYOUNGCHILDHH'] = df.apply(lambda x: 2015 if 'children' in x['TYPHH'] and 'child' in x['PLHH'] else None, axis=1)
    df['GEBMAANDJONGSTEKINDHH'] = df.apply(lambda x: '01' if 'children' in x['TYPHH'] and 'child' in x['PLHH'] else '--', axis=1)
    df['GEBJAAROUDSTEKINDHH'] = df.apply(lambda x: 2010 if 'children' in x['TYPHH'] and 'child' in x['PLHH'] else None, axis=1)
    df['BMAANDOUDSTEKINDHH'] = df.apply(lambda x: '05' if 'children' in x['TYPHH'] and 'child' in x['PLHH'] else '--', axis=1)

    return df

process_household(hh_df).to_csv(os.path.join('synth', 'data', 'raw', 'household_bus.csv'),
                                index=False)
    