import pandas as pd
import os

def preprocess():
    # read in raw data file
    df = pd.read_csv(os.path.join('synth', 'data', 'raw', 'hoogsteopl_tab.csv'),
                   index_col = False)

    # get all columns except for year
    group_columns = [col for col in df.columns if col not in ['year', 'OPLNRHB', 'OPLNRHG'] ]

    # do a full group by on all columns except year and keep only distinct rows
    df_grouped = df.groupby(group_columns, as_index=False).agg({'year': 'min'})
    df_grouped_sorted = df_grouped.sort_values(by='year', ascending=True)

    # save preprocessed data file
    df_grouped_sorted.to_csv(
        os.path.join('synth', 'data', 'raw', 'hoogsteopl_tab_cleaned.csv'), index=False)

if __name__ == "__main__":
    preprocess()