import pandas as pd
import sys

def preprocess(input_file, output_file):
    # read in raw data file
    df = pd.read_csv(input_file)

    # temporarily remove year
    year_column = df['Year']
    df_without_year = df.drop(columns='Year')

    # do a full group by on all columns except year and keep only distinct rows
    grouped_df = df_without_year.drop_duplicates()
    grouped_df['Year'] = year_column

    # save preprocessed data file
    grouped_df.to_csv(output_file, index=False)

    # display the resulting df (optional)
    print(grouped_df)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python preprocess.py <input file path> <output file path>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] 
        preprocess(input_file, output_file)