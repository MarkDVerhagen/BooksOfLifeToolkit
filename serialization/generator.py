from serial.HouseholdEventParagraph import HouseholdEventParagraph
from serial.PersonAttributesParagraph import PersonAttributesParagraph
import yaml
import requests
import pandas as pd

simulator.datasets

class Simulator:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.datasets = self.config.get('datasets', [])

    def pull_hierarchy(data, hierarchy_vars=['HOUSEKEEPING_NR', 'DATE_STIRTHH'],
                       main_key='rinpersoon', hierarchy_cat=None):
        ## Function to pull in main keys based on a hierarchy variable
        
        # Make hierarchy variable
        data['hierarchy'] = data.\
            apply(lambda row: '_'.join([str(row[var]) for var in hierarchy_vars]), axis=1)
            
        # Group by hierarchy and additional var
        hierarchy_list = ['hierarchy']
        if hierarchy_cat:
            hierarchy_list.append(hierarchy_cat)

        grouped = data.groupby(hierarchy_list).agg({main_key: list}).reset_index()

        # Pivot table
        if hierarchy_cat:
            grouped = grouped.pivot(index='hierarchy', columns=hierarchy_cat, values=main_key).reset_index()

        # Renaem columns
        grouped.columns.name = None
        grouped.columns = ['hierarchy'] + [f'ID_list_{col}' for col in grouped.columns if col != 'hierarchy']
        return pd.merge(data, grouped)

    def load_datasets(self):
        source = dataset['source']
        data = pd.read_csv(source)
        
        if dataset['social_structure']:
            pull_hierarchy(data, hierarchy_vars=dataset['social_structure'],
                           main_key=simulator.config['main_key'])
        
        return dataset

    def generate_sequence(self):
        ## order all events
        ## generate sequence
        
        sequence = []
        
        return sequence

# Example usage
yaml_file = os.path.join('synth', 'simple_recipe.yaml')
simulator = Simulator(yaml_file)
source = simulator.datasets[0]['source']

dataset = simulator.datasets[0]

simulator.show_attributes()
datasets = simulator.load_datasets()

# Access a specific dataset
iris_data = datasets.get('Iris')
if iris_data is not None:
    print(iris_data.head())
