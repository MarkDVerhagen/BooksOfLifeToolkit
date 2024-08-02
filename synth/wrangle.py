import pandas as pd
import os

hh = pd.read_csv(os.path.join('data', 'raw', 'household_bus_100.csv'),
                   index_col = False)
persoon = pd.read_csv(os.path.join('data', 'raw', 'persoon_tab_100.csv'),
                   index_col = False)
spolis = pd.read_csv(os.path.join('synth', 'data', 'raw', 'spolis_bus.csv'),
                   index_col = False)
hoogsteopl = pd.read_csv(os.path.join('data', 'raw', 'hoogsteopl_tab_100.csv'),
                   index_col = False)





persoon['rinpersoon'].isin(hh['rinpersoon']).mean()
hh['rinpersoon'].isin(persoon['rinpersoon']).mean()
spolis['rinpersoon'].isin(persoon['rinpersoon']).mean()
hoogsteopl['rinpersoon'].isin(persoon['rinpersoon']).mean()

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
