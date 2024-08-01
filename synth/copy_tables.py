import pandas as pd
import os
import numpy as np
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor

copy_times = 100  ## Factor 10
loops = np.ceil(np.log10(copy_times))
ids = ['rinpersoon', 'HOUSEKEEPING_NR']

# Raw and edit file dictionaries
files_dict = {
    'raw': ['household_bus', 'persoon_tab', 'spolis_bus', 'hoogsteopl_tab'],
    'edit': ['household_bus', 'persoon_tab', 'employment_bus', 'education_bus'],
}

def process_file(k, f, l):
    print(f"Doing {f}")
    if l == 0:
        file_suff = ''
    else:
        file_suff = '_' + str(pow(10, l))
        
    input_path = os.path.join('data', k, f + file_suff + '.csv')
    print(f"Read {input_path}")
    
    data = pd.read_csv(input_path, index_col=False)
    temp = deepcopy(data)
    for i in range(10):
        # print(f"Unique rinpersoon: {len(data['rinpersoon'].unique())}")
        suffix = str(i)
        for c in ids:
            try:
                data[[c]] = data[[c]] + suffix
            except KeyError:
                # print(f"Skipping {c}")
                continue
        data = pd.concat([data, temp])
    output_path = os.path.join('data', k, f + '_' + str(pow(10, l+1)) + '.csv')
    data.to_csv(output_path)
    print(f"Saved {output_path}")

# Function to handle parallel execution
def parallel_process(loop=1):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for k in files_dict:
            for f in files_dict[k]:
                futures.append(executor.submit(process_file, k, f, l))
        for future in futures:
            future.result()

if __name__ == "__main__":
    for l in range(int(loops)):
        parallel_process()
