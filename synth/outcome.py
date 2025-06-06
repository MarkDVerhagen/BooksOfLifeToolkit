# This file creates synthetic outcome data.
# It randomly assigns 5% of synthetic observations an outcome of 1.

import pandas as pd
import numpy as np

np.random.seed(111)

# Read in persoontab
persoontab = pd.read_csv('synth/data/raw/persoon_tab.csv')

# Create a new dataframe with the 'rinpersoon' column
outcome_df = persoontab[['rinpersoon']].copy()

# Add the 'outcome' column with approximately 5% of rows receiving the value 1
outcome_df['outcome'] = np.random.choice([0, 1], size=len(outcome_df), p=[0.95, 0.05])

# Save as csv
outcome_df.to_csv('synth/data/raw/outcome.csv', index=False)
