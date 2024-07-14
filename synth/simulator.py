import yaml
import requests
import pandas as pd

class Simulator:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.datasets = self.config.get('datasets', [])

    def fetch_dataset(self, source):
        try:
            response = requests.get(source)
            response.raise_for_status()
            return pd.read_csv(response.url)
        except requests.RequestException as e:
            print(f"Error fetching dataset from {source}: {e}")
            return None

    def pull_hierarchy(data, hierarchy_vars=['HOUSEKEEPING_NR', 'DATE_STIRTHH'],
                   hierarchy_cat=None, main_key='rinpersoon'):
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
        pivoted = grouped.pivot(index='hierarchy', columns=hierarchy_cat, values=main_key).reset_index()

        # Renaem columns
        pivoted.columns.name = None
        pivoted.columns = ['hierarchy'] + [f'ID_list_{col}' for col in pivoted.columns if col != 'hierarchy']
        return pd.merge(data, pivoted)
    
    
    def load_datasets(self):
        ## Generate self-degree time sequence
        ## Include self-degree information
        ## Fetch and add hierarchy to each event
        ## Fetch and add information for each fetched hierarchy element

    def generate_sequence(self):
        ## order all events
        ## generate sequence
        
        sequence = []
        
        return sequence

# Example usage
yaml_file = 'datasets.yaml'
simulator = Simulator(yaml_file)
simulator.show_attributes()
datasets = simulator.load_datasets()

# Access a specific dataset
iris_data = datasets.get('Iris')
if iris_data is not None:
    print(iris_data.head())
