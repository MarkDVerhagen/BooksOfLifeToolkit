import argparse
import os
import json
import numpy as np
import pandas as pd

def gen_fertility_probs(test_dir):
    # Read in population and fertility data
    start_pop = pd.read_csv(os.path.join(test_dir, 'data', 'age_sex_2023.csv'))
    fertility = pd.read_csv(os.path.join(test_dir, 'data', 'fertility_mothers_age_2023.csv'))
    fertility = fertility.rename(columns={'mothers_age': 'age'})
    
    # Reshape and merge the data
    start_pop = pd.melt(start_pop, id_vars=['variable'], var_name='age', value_name='n')
    start_pop['age'] = start_pop['age'].astype(int)
    df = pd.merge(start_pop, fertility, on='age') 
    df['birth_year'] = 2023 - df['age']
    df['fertility_prob'] = df['births'] / df['n']
    df = df.rename(columns={'variable': 'GBAGESLACHT',
                            'birth_year': 'GBAGEBOORTEJAAR'})
    df['sample_weight'] = df['n'] / df['n'].sum()
    
    return df[['GBAGESLACHT', 'GBAGEBOORTEJAAR', 'sample_weight', 'fertility_prob']]

def gen_books(df, test_dir, sample_n=250000):
    # Sample from the DataFrame
    sample = df.sample(sample_n, weights='sample_weight', random_state=1704, replace=True)
    
    sample['RINPERSOON'] = range(sample.shape[0])
    # Write each row as a JSON object to a JSONL file
    with open(os.path.join(test_dir, 'output', f'sample_{sample_n}.jsonl'), 'w') as jsonl_file:
        for _, person in sample.iterrows():
            pdict = {
                "rinpersoon": person["RINPERSOON"],
                "book_content": f"\n\nGender: {person['GBAGESLACHT']}\nYear of Birth: {person['GBAGEBOORTEJAAR']}",
                "outcome": str(int(np.random.uniform() <= person['fertility_prob'])),
            }
            jsonl_file.write(json.dumps(pdict) + '\n')

def main(test_dir, sample_n=250000):
    # Generate the fertility probabilities DataFrame
    df = gen_fertility_probs(test_dir)
    
    # Generate the books and write to JSONL
    gen_books(df, test_dir, sample_n)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a sample of Books of Life for correctness tests')
    parser.add_argument('--sample_size', type=int, default=25000, help='Define size of the sample.')
    args = parser.parse_args()

    # Define the directory containing the test data
    test_dir = os.path.join('tests', 'correctness')
    
    # Call the main function
    main(test_dir, sample_n=args.sample_size)
