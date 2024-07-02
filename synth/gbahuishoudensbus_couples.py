import random
from datetime import datetime, timedelta
from synth.params import synth_params
import json
from copy import copy
import os
import pandas as pd
import numpy as np
from datetime import datetime

with open(os.path.join('synth', 'hashed_hh_ids_' + str(synth_params['N_households']) + '.json'), 'r') as f:
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

class HouseholdMember:
    def __init__(self, id, place):
        self.id = id
        self.place = place

class Household:
    def __init__(self, id, members=[]):
        self.id = id
        self.members = members
        self.spells = []
        self.household_type = self.assign_household_type()
        self.generate_members_based_on_type()
    
    def assign_household_type(self):
        types = [
            'single person household',
            'couple with children',
            'couple without children',
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
        household = Household('{:08d}'.format(n))
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

def simulate_movement(households):
    events = ['breakup',  # household dissolves into two
              'child_born',  # household is retained and expanded
              'couple_formed',  # mew household is generated
              'nothing']  # household is retained
    
    probs = {'single person household': [0, 0.05, 0.65, 0.3],
             'couple without children': [0.4, 0.25, 0, 0.35],
             'couple with children': [0.2, 0.05, 0, 0.75],
             'single parent household': [0, 0.01, 0.5, 0.49]}
    
    for i in range(len(households)):
        hh = households[i]
        event_probs = probs[hh.household_type]
        event = np.random.choice(events, p=event_probs)
        
        if event == 'nothing':
            hh.spells = [hh.spells[-1], datetime(hh.spells[-1].year + 1, 1, 1)]
            households.append(hh)
        if event == 'child_born':
            hh.spells = [hh.spells[-1], datetime(hh.spells[-1].year + 1, 1, 1)]
            hh.members.append(HouseholdMember(id = hash_set.pop(),
                                              place = place_descriptions[1]))
            for m in hh.members:
                m.place = child_born_map[m.place]
            
            hh.household_type = assign_household_type(hh)
            households.append(hh)
        if event == 'breakup':
            
            children = [h for h in hh.members if h.place == 'child living at home']
            parents = [h for h in hh.members if h.place != 'child living at home']
            
            old_hh = copy(hh)
            old_hh.members = [parents[0]] + children
            
            old_hh.spells = [hh.spells[-1], datetime(hh.spells[-1].year + 1, 1, 1)]
            old_hh.household_type = assign_household_type(old_hh)
            
            new_hh = Household(id = household_hash_set.pop(),
                               members = parents[1],
                               )
            new_hh.household_type = 'single person household'
            
            new_hh.spells = [hh.spells[-1], datetime(hh.spells[-1].year + 1, 1, 1)]
            
            households.append(new_hh)
            households.append(old_hh)
    return households


# Load hashed set of individuals

with open(os.path.join('synth', 'hashed_ids_' + str(synth_params['N']) + '.json'), 'r') as f:
    hash_set = json.load(f)

N_households = synth_params['N_households']

households = generate_initial_households(N_households)

[h.place for h in households[1].members]

households2 = simulate_movement(households)


len(households2)


simulate_movement(households2)