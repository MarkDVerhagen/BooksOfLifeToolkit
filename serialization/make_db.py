import yaml
import pandas as pd
import os

class Generator:
    def __init__(self, yaml_file, data_dir='data'):
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.datasets = self.config.get('datasets', [])
        self.main_key = self.config.get('main_key', [])
        self.data_dir = data_dir

        for d in self.datasets:
            print('Now doing {}'.format(d['name']))
            data = pd.read_csv(os.path.join(self.data_dir, 'raw', d['name']))

            structure_features = d.get('structure_features')
            structure_class = d.get('structure_classification')
            if structure_features:
                print('Adding structure features to {}'.format(d['name']))
                print(structure_features)
                data = self.pull_hierarchy(
                    data, hierarchy_vars=structure_features,
                    main_key=self.main_key, hierarchy_cat=structure_class)
            
            data.to_csv(os.path.join(self.data_dir, 'edit', d['name']))
    
    
    def pull_hierarchy(self, data, hierarchy_vars=['HOUSEKEEPING_NR', 'DATE_STIRTHH'],
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


if __name__ == "__main__":    
    # Example usage
    yaml_file = os.path.join('recipes', 'template.yaml')
    data_path = os.path.join('synth', 'data')
    Generator(yaml_file, data_dir=data_path)