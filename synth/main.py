import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class HouseholdMember:
    def __init__(self, id, place):
        self.id = id
        self.place = place  # New attribute to store the member's place

class Household:
    def __init__(self, id, members=[]):
        self.id = id
        self.members = members
        self.spells = []
        self.household_type = self.assign_household_type()
        self.generate_members_based_on_type()
    
    def assign_household_type(self):
        types = [
            "unknown", "single person household", "not married couple without children",
            "married couple without children", "not married couple with children",
            "married couple with children", "single parent household",
            "other household", "institutional household"
        ]
        return random.choice(types)
    
    def generate_members_based_on_type(self):
        place_descriptions = {
            1: "child living at home",
            2: "single person",
            3: "non-married partner in couple without children",
            4: "married partner in couple without children",
            5: "non-married partner in couple with children",
            6: "married partner in couple with children",
            7: "parent in single parent household",
            8: "reference person in other household type",
            9: "other member in household",
            10: "member of an institutional household"
        }
        
        type_to_places = {
            "single person household": [2],
            "not married couple without children": [3, 3],
            "married couple without children": [4, 4],
            "not married couple with children": [5, 5] + [1] * random.randint(1, 3),
            "married couple with children": [6, 6] + [1] * random.randint(1, 3),
            "single parent household": [7] + [1] * random.randint(1, 3),
            "other household": [8] + [9] * random.randint(2, 4),
            "institutional household": [10] * random.randint(4, 10),
            "unknown": [9] * random.randint(2, 5)
        }
        
        places = type_to_places.get(self.household_type, [9])
        self.members = [HouseholdMember(f"{self.id}_{i+1}", place_descriptions[place]) for i, place in enumerate(places)]
    
    def start_new_spell(self, start_date):
        if self.spells:
            self.spells[-1]['end_date'] = start_date - timedelta(days=1)
        self.spells.append({
            'start_date': start_date,
            'end_date': datetime(2050, 1, 1),
            'members': [(member.id, member.place) for member in self.members],
            'household_type': self.household_type
        })
        
    def reassign_household_type(self):
        # Simplified logic to reassess household type based on members' places
        if not self.members:
            self.household_type = "unknown"
        elif len(self.members) == 1:
            self.household_type = "single person household"
            self.members[-1].place = "single person"
        elif 'couple' in self.household_type:
            child_count = sum(1 for member in self.members if member.place == "child living at home")
            adult_count = len(self.members) - child_count
            if adult_count == 1 and child_count > 0:
                self.household_type = "single parent household"
            elif adult_count >= 2 and child_count == 0:
                self.household_type = random.choice(["married couple without children",
                                                     "non-married couple without children"])
            elif adult_count >= 2 and child_count > 0:
                self.household_type = random.choice(["married couple with children",
                                                     "non-married couple with children"])
            else:
                self.household_type = "other household"
        else:
            ## Other or institutional
            self.household_type = self.household_type
    
        if self.household_type == "unknown":
            for member in self.members:
                member.place = "other member in household"
        
        if self.household_type == "other household":
            for member in self.members:
                member.place = "other member in household"
            
            self.members[-1].place = "reference person in other household type"
            
        if self.household_type == "institutional household":
            for member in self.members:
                member.place = "member of an institutional household"


def generate_initial_households(N):
    households = []
    for n in range(N):
        household = Household("{:08d}".format(n))
        household.start_new_spell(datetime(2020, 1, 1))
        households.append(household)
    return households

def simulate_movements(households, num_movements):
    
    while num_movements > 0:
        # Randomly choose a member from a household to move
        leaving_household = random.choice(households)
        if not leaving_household.members:
            continue  # Skip if household has no members
        
        current_date = leaving_household.spells[-1]["start_date"] + timedelta(days=random.randint(30, 90))
        
        moving_member = leaving_household.members.pop(random.randint(0, len(leaving_household.members) - 1))
        
        leaving_household.reassign_household_type()  # Reassign type after member removal

        # Decide if joining an existing household or forming a new one
        if random.random() < 0.5 and len(households) > 1:
            # Join an existing household
            receiving_household = random.choice([hh for hh in households if hh != leaving_household])
            receiving_household.members.append(moving_member)
            receiving_household.reassign_household_type()  # Reassign type after member addition
            receiving_household.start_new_spell(current_date)
        else:
            # Form a new household
            new_household = Household(f"HH{len(households)+1}")
            new_household.members.append(moving_member)
            new_household.reassign_household_type()  # Ensure correct type for new household
            new_household.start_new_spell(current_date)
            households.append(new_household)

        leaving_household.start_new_spell(current_date)
        
        current_date += timedelta(days=random.randint(30, 90))  # Move every 1 to 3 months
        num_movements -= 1


def collect_data_for_dataframe_separate_rows(households):
    data = []
    for household in households:
        for spell in household.spells:
            for member_id in spell['members']:
                data.append({
                    'Household ID': household.id,
                    'Household type': spell["household_type"],
                    'Household Member ID': member_id[0],
                    'Household Member place': member_id[1],
                    'Start Date': spell['start_date'],
                    'End Date': spell['end_date'] if spell['end_date'] else datetime(2050, 1, 1)  # Handling ongoing spells
                })
    return data

# Example usage
N = 1000  # Initial number of households
households = generate_initial_households(N)
simulate_movements(households, num_movements=1000)

# Convert the collected data into a pandas DataFrame
data_for_df = collect_data_for_dataframe_separate_rows(households)
household_df = pd.DataFrame(data_for_df)

household_df.to_csv('gbahuishoudensbus.csv', index=False)