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
