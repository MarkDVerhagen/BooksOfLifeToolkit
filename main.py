import duckdb
import multiprocessing
import pandas as pd
import random
import os
from serialization.BookofLifeGenerator import BookofLifeGenerator
import time
import traceback
from tqdm import tqdm
import argparse
import json
from utils.summary import generate_token_length_stats

def generate_and_save_book_wrapper(args):
    """Wrapper function to unpack arguments for generate_and_save_book."""
    return generate_and_save_book(*args)

def get_unique_rinpersoons(db_path):
    """Fetch all unique rinpersoon IDs from the persoon_tab table."""
    try:
        conn = duckdb.connect(db_path, read_only=True)

        # Check if the table exists
        table_exists = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='persoon_tab'").fetchone()
        if not table_exists:
            print(f"Table 'persoon_tab' does not exist in the database.")
            return []

        # Fetch and print the number of rows
        row_count = conn.execute("SELECT COUNT(*) FROM persoon_tab").fetchone()[0]
        print(f"Number of rows in persoon_tab: {row_count}")

        # Fetch all rinpersoon values
        result = conn.execute("SELECT DISTINCT rinpersoon FROM persoon_tab").fetchall()
        rinpersoons = [row[0] for row in result]
        return rinpersoons
    except Exception as e:
        print(f"Database error: {e}")
        return []

def generate_and_save_book(rinpersoon, recipe_yaml_path, outcome_dict):
    """Generate a Book of Life for a single rinpersoon and include the outcome."""
    try:
        generator = BookofLifeGenerator(rinpersoon, recipe_yaml_path=recipe_yaml_path)
        book_content = generator.generate_book()
        outcome = outcome_dict.get(rinpersoon, "0")  # Default to "0" if not found
        return rinpersoon, book_content, outcome
    except Exception as e:
        print(f"Error generating Book of Life for rinpersoon {rinpersoon}: {str(e)}")
        print(traceback.format_exc())
        return rinpersoon, None, None

def save_to_jsonl_shard(data, output_dir, shard_index):
    """Save a shard of data to a JSONL file."""
    shard_filename = f"shard_{shard_index}.jsonl"
    shard_path = os.path.join(output_dir, shard_filename)
    
    with open(shard_path, 'a') as jsonl_file:
        json_record = {
            "rinpersoon": data[0],
            "book_content": data[1],
            "outcome": data[2]
        }
        jsonl_file.write(json.dumps(json_record) + '\n')

def process_and_save_books(rins, recipe_yaml_path, output_dir, shard_size, pool, outcome_dict):
    """Process books and save them to shards on the go."""
    for i, result in enumerate(tqdm(pool.imap(generate_and_save_book_wrapper, [(rin, recipe_yaml_path, outcome_dict) for rin in rins]), total=len(rins))):
        save_to_jsonl_shard(result, output_dir, i // shard_size)

def main(bol_name, recipe_name, max_processes=None, shard_size=1000, output_dir=None, save_summary=False):
    # check if data directory for this bol_name already exists
    if os.path.exists(bol_name):
        raise ValueError(f"Data directory for {bol_name} already exists.")

    # Print number of unique rinpersoons
    db_path = 'synthetic_data.duckdb'
    unique_rinpersoons = get_unique_rinpersoons(db_path)
    print(f"Number of unique rinpersoons: {len(unique_rinpersoons)}")

    synth_hh = pd.read_csv(os.path.join('synth', 'data', 'edit', 'household_bus.csv'))
    
    # Filter and process data
    synth_hh = synth_hh[synth_hh['DATE_STIRTHH'] == '1998-01-01']
    final_year_rins = synth_hh['rinpersoon'][synth_hh['PLHH'] != 'child living at home'].unique()
    final_year_hhs = synth_hh['HOUSEKEEPING_NR'].unique()
    
    # Split into train and test sets
    train_hhs = random.sample(list(final_year_hhs), round(0.8*len(final_year_hhs)))
    test_hhs = [i for i in final_year_hhs if i not in train_hhs]
    train_rins = list(synth_hh['rinpersoon'][synth_hh['HOUSEKEEPING_NR'].isin(train_hhs)])
    test_rins = list(synth_hh['rinpersoon'][~synth_hh['HOUSEKEEPING_NR'].isin(test_hhs)])
    train_rins = [i for i in train_rins if i in final_year_rins]
    test_rins = [i for i in test_rins if i in final_year_rins]
    
    # Process outcomes
    outcome = pd.read_csv(os.path.join('synth', 'data', 'edit', 'household_bus.csv'))
    outcome = outcome[outcome['DATE_STIRTHH'] == '1999-01-01']
    outcome_rins_1 = outcome['rinpersoon'][outcome['EVENT'] == 'child_born']
    
    # Create outcome dictionary
    outcome_dict = {rin: 1 if rin in outcome_rins_1.values else 0 for rin in final_year_rins}
        
    num_processes = min(max_processes or multiprocessing.cpu_count(), multiprocessing.cpu_count())
    print(f"Using {num_processes} processes for parallel generation.")
    
    print(f"\n\nGenerating Books of Life with outcomes for recipe: {recipe_name}\n----------")
    recipe_yaml_path = f'./recipes/{recipe_name}.yaml'
    
    # Set up directory structure
    if output_dir is not None:
        bol_name = os.path.join(output_dir, bol_name)
    base_dir = os.path.join(bol_name, 'data')
    train_dir = os.path.join(base_dir, 'train')
    test_dir = os.path.join(base_dir, 'test')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    with multiprocessing.Pool(processes=num_processes) as pool:
        print("Generating and saving train Books of Life with outcomes:")
        process_and_save_books(train_rins, recipe_yaml_path, train_dir, shard_size, pool, outcome_dict)
        
        print("Generating and saving test Books of Life with outcomes:")
        process_and_save_books(test_rins, recipe_yaml_path, test_dir, shard_size, pool, outcome_dict)

    # store recipe file in data directory
    os.system(f"cp {recipe_yaml_path} {base_dir}")

    print("All Books of Life with outcomes have been generated and saved in JSONL shards.")

    # Generate token length statistics
    print("\nGenerating token length statistics for the generated Books of Life:")
    generate_token_length_stats(base_dir, sample_size=10000, save_to_file=save_summary)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--bol_name", type=str, required=True, help="Name of the Book of Life data repository that is stored.")
    args.add_argument("--recipe_name", type=str, required=True, help="Name of the recipe file to use. This should be stored in the recipe directory.")
    args.add_argument("--max_processes", type=int, default=4, help="Maximum number of processes to use for parallel generation.")
    args.add_argument("--shard_size", type=int, default=10000, help="Number of entries per shard.")
    args.add_argument("--output_dir", type=str, default=None, help="Output directory to save the data directory.")
    args.add_argument("--save_summary", action='store_true', help="Whether to save the token length statistics summary to the data directory after generation.")
    args = args.parse_args()

    start_time = time.time()
    main(**vars(args))
    print(f"Execution time: {round((time.time() - start_time)/60, 2)} mins.")