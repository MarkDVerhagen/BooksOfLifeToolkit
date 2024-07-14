import pandas as pd
import os

data = pd.read_csv(os.path.join('synth', 'data', 'householdbus.csv'),
                   index_col = False).drop(columns=['Unnamed: 0'])

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

pull_hierarchy(data).to_csv(
    os.path.join('synth', 'data', 'householdbus_structure.csv'),
)
