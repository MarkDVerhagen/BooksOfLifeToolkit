import hashlib
import json
import random
import string
import os
from synth.params import synth_params

def generate_hashed_id(length=8):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    hashed_id = hashlib.sha256(random_string.encode()).hexdigest()[:length]
    return hashed_id

def generate_n_hashed_ids(n, seed, hash_length=8):
    random.seed(seed)
    ids = [generate_hashed_id(length=hash_length) for _ in range(n)]
    return ids

# Specify the number of IDs you want to generate
N = synth_params["N_hash"]
seed = synth_params["seed"]
hashed_ids = generate_n_hashed_ids(N, seed, hash_length=8)

with open(os.path.join('synth', 'hashed_ids_' + str(N) + '.json'), 'w') as f:
    json.dump(hashed_ids, f)


# Specify the number of hosusehold IDs you want to generate
N = synth_params["N_hh_hash"]
seed = synth_params["seed"]
hashed_ids = generate_n_hashed_ids(N, seed, hash_length=8)

with open(os.path.join('synth', 'hashed_hh_ids_' + str(N) + '.json'), 'w') as f:
    json.dump(hashed_ids, f)


# Specify the number of firm IDs you want to generate
N = synth_params["N_firms"]
seed = synth_params["seed"]
hashed_ids = generate_n_hashed_ids(N, seed, hash_length=8)

with open(os.path.join('synth', 'hashed_firm_ids_' + str(N) + '.json'), 'w') as f:
    json.dump(hashed_ids, f)
