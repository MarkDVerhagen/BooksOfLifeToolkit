import numpy as np
import os
import pandas as pd
import json
from params import synth_params

# Set simulation parameters
with open(os.path.join('synth', 'hashed_firm_ids_' + str(synth_params['N_firms']) + '.json'), 'r') as f:
    firm_ids = json.load(f)
T = 5*12  # Number of months to simulate

employment_prob_dict = {
    'unemployed': 0.2,
    'employed': 0.98,
}

# Setup starting data
persoon_tab = pd.read_csv('./synth/data/raw/persoon_tab.csv')[['rinpersoon', 'GBAGEBOORTEJAAR']]

data = {
    'rinpersoon': persoon_tab['rinpersoon'],
    'year': 2010, 
    'birth_year': persoon_tab['GBAGEBOORTEJAAR'],
    'month': 0,
}

df = pd.DataFrame(data)
df['employment_status'] = df['birth_year'].apply(
    lambda x: 'employed' if x <= 1992 and np.random.rand() < 0.95 else 'unemployed')
df['firm_id'] = df['employment_status'].apply(
    lambda x: np.random.choice(firm_ids) if x == 'employed' else np.nan)

# Function to simulate employment status for T months
def simulate_employment(df, T, employment_prob_dict):
    simulation_results = []
    for t in range(T):
        temp = df.loc[df['month'] == (t - 1)]
        
        employment_status_copy = temp['employment_status'].copy()

        temp['new_status'] = employment_status_copy.apply(
            lambda x: 'unemployed' if x == 'employed' and np.random.rand() < employment_prob_dict['unemployed']
            else ('employed' if x == 'unemployed' and np.random.rand() < employment_prob_dict['employed'] else x)
        )
        
        temp.loc[:, 'new_firm_id'] = temp.loc[:, 'firm_id'].copy()
        
        temp['new_firm_id'] = temp.apply(
            lambda x: np.random.choice(firm_ids) if (x['new_status'] != x['employment_status']) and
            x['new_status'] == 'employed' else x['firm_id'], axis=1)
        
        temp['new_firm_id'] = np.where(temp['new_status'] == 'unemployed', np.nan,
                                       temp['new_firm_id'])
        
        temp['month'] = t
        temp = temp.drop(columns = ['employment_status', 'firm_id'])
        temp = temp.rename(columns ={'new_status': 'employment_status',
                                     'new_firm_id': 'firm_id'})
        df = pd.concat([df, temp[['rinpersoon', 'year', 'month', 'employment_status', 'firm_id']]])
        
    return df

# Run the simulation
results = simulate_employment(df, T, employment_prob_dict)
results = results.drop(columns = ['birth_year', 'year'])

# Make date columns
results = results.assign(year = 2010 + results['month'] % 12)
results = results.assign(month = (results['month'] % 12) + 1)
results = results.loc[results['employment_status'] != 'unemployed']
results = results.assign(salary = [np.random.randint(1000, 10000) for i in range(results.shape[0])])

# # Initialize additional columns with random data for simulation purposes
# results['SIMPUTATIE'] = np.random.choice(['J', 'N', '-'], len(results))
# results['SINDWAARNEMING'] = np.random.choice(['0', '1'], len(results))
# results['SDATUMAANVANGIKO'] = (pd.to_datetime('today') - pd.to_timedelta(np.random.randint(0, 365, len(results)), unit='d')).strftime('%Y-%m-%d')
# results['SDATUMAANVANGIKV'] = results['SDATUMAANVANGIKO']
# results['SDATUMAANVANGIKVORG'] = results['SDATUMAANVANGIKO']
# results['SDATUMEINDEIKO'] = (pd.to_datetime('today') + pd.to_timedelta(np.random.randint(0, 365, len(results)), unit='d')).strftime('%Y-%m-%d')
# results['SDATUMEINDEIKV'] = results['SDATUMEINDEIKO']
# results['SBAANDAGEN'] = np.random.randint(1, 366, len(results))
# results['SVOLTIJDDAGEN'] = np.random.randint(1, 366, len(results))
# results['SAANTSV'] = np.random.randint(1, 366, len(results))
# results['SREGULIEREUREN'] = np.random.randint(0, 40, len(results))
# results['SWEKARBDUURKLASSE'] = np.random.choice(["1", "2", "3", "4", "5", "6"], len(results))
# results['SAANTCTRCTURENPWK'] = np.random.randint(0, 40, len(results))
# results['SAANTVERLU'] = np.random.randint(0, 40, len(results))
# results['SBASISUREN'] = np.random.randint(0, 40, len(results))
# results['SOVERWERKUREN'] = np.random.randint(0, 20, len(results))
# results['SFSINDFZ'] = np.random.choice(["--", "00", "01", "02", "03", "04", "05", "06", "17", "18", "19", "38", "40", "41", "42", "43", "44"], len(results))
# results['STIJDVAKTYPE'] = np.random.choice(["1", "3", "4", "5"], len(results))
# results['SPOLISDIENSTVERBAND'] = np.random.choice(["1", "2"], len(results))
# results['SARBEIDSRELATIE'] = np.random.choice(["1", "2"], len(results))
# results['SOVERWERK'] = np.random.choice(["0", "1"], len(results))
# results['INDPUBAANONBEPTD'] = np.random.choice(["J", "N"], len(results))
# results['SCAOSECTOR'] = np.random.choice(["1000", "2000", "3000", "3100", "3200", "3210", "3211", "3212", "3213", "3220", "3230", "3240", "3250", "3290", "3300", "3310", "3320", "3400", "3500", "3600", "3700", "3800"], len(results))
# results['SSECT'] = np.random.choice(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "99"], len(results))
# results['SSOORTBAAN'] = np.random.choice(["1", "2", "3", "4", "5", "9"], len(results))
# results['SWGHZVW'] = np.random.uniform(0, 1000, len(results))
# results['PrAwfLg'] = np.random.uniform(0, 1000, len(results))
# results['PrAwfHg'] = np.random.uniform(0, 1000, len(results))
# results['PrAwfHz'] = np.random.uniform(0, 1000, len(results))
# results['SBASISLOON'] = np.random.uniform(0, 10000, len(results))
# results['SCTRCTLN'] = np.random.uniform(0, 10000, len(results))
# results['SSRTIV'] = np.random.choice(["11", "12", "13", "14", "15", "17", "18", "21", "22", "23", "24", "31", "32"], len(results))
# results['SINCIDENTSAL'] = np.random.uniform(0, 1000, len(results))
# results['SCDINCINKVERM'] = np.random.choice(["--", "B", "G", "O", "S", "Z"], len(results))
# results['SLNINGLD'] = np.random.uniform(0, 10000, len(results))
# results['SWRDLN'] = np.random.uniform(0, 1000, len(results))
# results['PRLNUFO'] = np.random.uniform(0, 1000, len(results))
# results['PRLNAWFANWLg'] = np.random.uniform(0, 1000, len(results))
# results['PRLNAWFANWHg'] = np.random.uniform(0, 1000, len(results))
# results['PRLNAWFANWHz'] = np.random.uniform(0, 1000, len(results))
# results['PRLNAOFANWHG'] = np.random.uniform(0, 1000, len(results))
# results['PRLNAOFANWLG'] = np.random.uniform(0, 1000, len(results))
# results['PRLNAOFANWUIT'] = np.random.uniform(0, 1000, len(results))
# results['SINDWAO'] = np.random.choice(["N", "J"], len(results))
# results['SINDWW'] = np.random.choice(["N", "J"], len(results))
# results['SLNSV'] = np.random.uniform(0, 10000, len(results))
# results['SRISGRP'] = np.random.choice(["--", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"], len(results))
# results['SINGLBPH'] = np.random.uniform(0, 10000, len(results))
# results['SLNLBPH'] = np.random.uniform(0, 10000, len(results))
# results['SCDINVLVPL1'] = np.random.choice(["--", "A", "B", "C", "D", "E", "F", "X"], len(results))
# results['SCDINVLVPL2'] = np.random.choice(["--", "A", "B", "C", "D", "E", "F", "X"], len(results))
# results['SCDINVLVPL3'] = np.random.choice(["--", "A", "B", "C", "D", "E", "F", "X"], len(results))
# results['SVERSTRAANV'] = np.random.uniform(0, 1000, len(results))
# results['SVERGZVW'] = np.random.uniform(0, 1000, len(results))
# results['SPENSIOENPREMIE'] = np.random.uniform(0, 1000, len(results))
# results['SBEDRZDAFTR'] = np.random.uniform(0, 1000, len(results))
# results['SBIJDRZVW'] = np.random.uniform(0, 1000, len(results))

results.to_csv(
    os.path.join('synth', 'data', 'raw', 'spolis_bus.csv'), index=False)
