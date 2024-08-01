import pandas as pd
from itertools import product
import os

def preprocess(group_columns = ['rinpersoon', 'year']):
    # read in raw data file
    df = pd.read_csv(os.path.join('synth', 'data', 'raw', 'spolis_bus.csv'),
                   index_col = False)
    
    # Get unique values for rinpersoon
    unique_ids = df['rinpersoon'].unique()

    # Define the full range of months and years
    all_months = range(1, 13)  # January (1) to December (12)
    all_years = range(min(df['year']), max(df['year']))  

    # create df with all combinations of rinpersoon, month, and year
    complete_combos = pd.DataFrame(list(product(unique_ids, all_months, all_years)), columns=['rinpersoon', 'month', 'year'])

    # merge with original df to fill in missing rows
    df_complete = pd.merge(complete_combos, df, on=['rinpersoon', 'month', 'year'], how='left')
    # replace NaN values in the 'employment_status' column with 'unemployed'
    df_complete['employment_status'] = df_complete['employment_status'].fillna('unemployed')
    
    df_cleaned = df_complete.groupby(group_columns).agg(
        num_employed_months = ('employment_status', lambda x: (x == 'employed').sum()),
        num_firms_worked_at = ('firm_id', lambda x: x.nunique(dropna=True)),
        average_salary_while_employed = ('salary', 'mean')
    ).reset_index()

    # save preprocessed data file
    df_cleaned.to_csv(
        os.path.join('synth', 'data', 'edit', 'employment_bus.csv'), index=False)

if __name__ == "__main__":
    preprocess()