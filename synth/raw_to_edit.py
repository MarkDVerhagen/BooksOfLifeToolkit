import pandas as pd
from itertools import product
import numpy as np
import sys
import os

### need to do some light preprocessing per raw file...e.g. turning '-' into NaNs, 
### turning codes into categorical vars, set binary vars? (e.g. employment status)

def preprocess(domain, track_changes_by = ["year"]):
    filetype = "yearly"
    # read in raw data file
    if domain == "education":
        df = pd.read_csv(os.path.join('synth', 'data', 'raw', 'hoogsteopl_tab_cleaned.csv'), index_col = False)
        output_file_name = "education_bus.csv"
    elif domain == "wealth":
        df = pd.read_csv(os.path.join('synth', 'data', 'raw', 'veh_tab.csv'), index_col = False)
        output_file_name = "wealth_tab.csv"
    elif domain == "employment":
        df = pd.read_csv(os.path.join('synth', 'data', 'raw', 'spolis_bus.csv'), index_col = False)
        output_file_name = "employment_bus.csv"
        filetype = "monthly"
        
    ## if file is month-type file, create empty rows for months that aren't in the data
    if filetype == "monthly":
        # Get unique values for rinpersoon
        unique_ids = df['rinpersoon'].unique()

        # Define the full range of months and years
        all_months = range(1, 13)  # January (1) to December (12)
        all_years = range(min(df['year']), max(df['year']))  

        # create df with all combinations of rinpersoon, month, and year
        complete_combos = pd.DataFrame(list(product(unique_ids, all_months, all_years)), columns=['rinpersoon', 'month', 'year'])
        complete_combos['quarter'] = complete_combos['month'].apply(determine_quarter)
        
        # merge with original df to fill in missing rows
        df = pd.merge(complete_combos, df, on=['rinpersoon', 'month', 'year'], how='left')
        
        for col in ['year', 'month', 'quarter']:
            df[col] = pd.Categorical(df[col], categories=sorted(df[col].unique()), ordered=True)
    else: 
        df['year'] = pd.Categorical(df['year'], categories=sorted(df['year'].unique()), ordered=True)
        
    if 'rinpersoon' not in track_changes_by:
        track_changes_by.append('rinpersoon')

    df_grouped = df.groupby(track_changes_by, observed=False)

    # Initialize lists to hold results
    results = []

    # Iterate over each group
    for name, group in df_grouped:
        # Create a dictionary to hold aggregated values for the current group
        agg_dict = dict(zip(track_changes_by, name))
        
        # For each column, perform aggregation
        for col in group.columns:
            if col in track_changes_by:
                continue
            
            series = group[col]
            
            # Numeric columns: compute mean (ignoring NaNs)
            if pd.api.types.is_numeric_dtype(series):
                mean_value = series.mean()
                agg_dict[f'mean_{col}'] = mean_value if pd.notna(mean_value) else np.nan

            # Categorical columns: count unique non-NaN values
            elif isinstance(series.dtype, pd.CategoricalDtype) or pd.api.types.is_object_dtype(series):
                num_unique = series.nunique(dropna=True)
                agg_dict[f'num_unique_{col}'] = num_unique if num_unique > 0 else np.nan
            # Skip unsupported types
            else:
                continue
        
        # Append the aggregated dictionary to the results list
        results.append(agg_dict)
    
    # Convert results to df
    df_cleaned = pd.DataFrame(results)

    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

    # Get unique non-NA values of each categorical column and store in agg_[column]
    for col in categorical_cols:
        if col in track_changes_by:
            continue
        # Compute unique values
        unique_values = df.groupby(track_changes_by, observed=False)[col].unique().reset_index()
        unique_values.rename(columns={col: f'agg_{col}'}, inplace=True)
        # Identify columns containing 'agg' in the name and remove NaNs
        agg_columns = [col for col in unique_values.columns if 'agg' in col]
        for col in agg_columns:
            unique_values[col] = unique_values[col].apply(remove_nans)
        # Merge unique values to get final cleaned df
        df_cleaned = pd.merge(df_cleaned, unique_values, on=track_changes_by, how='left')

    # save edited data file
    df_cleaned.to_csv(
        os.path.join('synth', 'data', 'edit', output_file_name), index=False)
    
# Function to determine the quarter of the year
def determine_quarter(month):
    if month in [1, 2, 3]:
        return 1
    elif month in [4, 5, 6]:
        return 2
    elif month in [7, 8, 9]:
        return 3
    elif month in [10, 11, 12]:
        return 4
    
# Function to remove NaNs from vector
def remove_nans(vector):
    return [x for x in vector if not pd.isna(x)]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 raw_to_edit.py <domain> <track_changes_by>")
    else:
        domain = sys.argv[1]
        track_changes_by_str = sys.argv[2:]
        track_changes_by = [str(arg) for arg in track_changes_by_str]
        preprocess(domain, track_changes_by)