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

global conn_dict
conn_dict = {}

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
    if multiprocessing.current_process().name not in conn_dict:
        print(f"Process {multiprocessing.current_process().name} is initializing a new connection to the database.")
        # copy the database to a new file for this process
        db_path = 'synthetic_data.duckdb'
        new_db_path = f'synthetic_data_{multiprocessing.current_process().name}.duckdb'
        os.system(f"cp {db_path} {new_db_path}")

        conn = duckdb.connect(":memory:")
        
        # copy the data from original database to new database without attaching the original database but by copying the data
        conn.execute(f"ATTACH DATABASE '{new_db_path}' AS new_db")
        
        # Get all table names from the attached database
        tables = conn.execute("SELECT table_name FROM new_db.information_schema.tables WHERE table_schema = 'main'").fetchall()
        
        # Create tables and copy data for each table
        for table in tables:
            table_name = table[0]
            conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM new_db.{table_name}")

        conn_dict[multiprocessing.current_process().name] = conn

        # remove the copied database file
        os.system(f"rm {new_db_path}")


    try:
        generator = BookofLifeGenerator(rinpersoon, recipe_yaml_path=recipe_yaml_path, duck_db_conn=conn_dict[multiprocessing.current_process().name])
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
    conn = duckdb.connect(db_path, read_only=True)
    unique_rinpersoons = get_unique_rinpersoons(db_path)
    print(f"Number of unique rinpersoons: {len(unique_rinpersoons)}")


    # Filter and process data
    conn.execute("""
        CREATE TEMPORARY TABLE synth_hh AS
        SELECT *
        FROM household_bus
        WHERE DATE_STIRTHH = '1998-01-01'
    """)

    final_year_rins = conn.execute("""
        SELECT DISTINCT rinpersoon
        FROM synth_hh
        WHERE PLHH != 'child living at home'
    """).fetchnumpy()['rinpersoon']

    final_year_hhs = conn.execute("""
        SELECT DISTINCT HOUSEKEEPING_NR
        FROM synth_hh
    """).fetchnumpy()['HOUSEKEEPING_NR']

    # Split into train and test sets
    train_size = round(0.8 * len(final_year_hhs))
    random.shuffle(final_year_hhs)
    train_hhs = final_year_hhs[:train_size]
    test_hhs = final_year_hhs[train_size:]

    # Create temporary tables for train and test households
    conn.execute("CREATE TEMPORARY TABLE train_hhs (HOUSEKEEPING_NR VARCHAR)")
    conn.executemany("INSERT INTO train_hhs VALUES (?)", [(hh,) for hh in train_hhs])

    conn.execute("CREATE TEMPORARY TABLE test_hhs (HOUSEKEEPING_NR VARCHAR)")
    conn.executemany("INSERT INTO test_hhs VALUES (?)", [(hh,) for hh in test_hhs])

    train_rins = conn.execute("""
        SELECT DISTINCT s.rinpersoon
        FROM synth_hh s
        JOIN train_hhs t ON s.HOUSEKEEPING_NR = t.HOUSEKEEPING_NR
        WHERE s.rinpersoon IN (SELECT UNNEST(?))
    """, [list(final_year_rins)]).fetchnumpy()['rinpersoon']

    test_rins = conn.execute("""
        SELECT DISTINCT s.rinpersoon
        FROM synth_hh s
        JOIN test_hhs t ON s.HOUSEKEEPING_NR = t.HOUSEKEEPING_NR
        WHERE s.rinpersoon IN (SELECT UNNEST(?))
    """, [list(final_year_rins)]).fetchnumpy()['rinpersoon']

    # Process outcomes
    outcome_rins_1 = conn.execute("""
        SELECT DISTINCT rinpersoon
        FROM household_bus
        WHERE DATE_STIRTHH = '1999-01-01' AND EVENT = 'child_born'
    """).fetchnumpy()['rinpersoon']

    # Create outcome dictionary
    outcome_dict = conn.execute("""
        WITH outcome_table AS (
            SELECT UNNEST(?) AS rinpersoon, 1 AS outcome
        )
        SELECT f.rinpersoon, COALESCE(o.outcome, 0) AS outcome
        FROM (SELECT UNNEST(?) AS rinpersoon) f
        LEFT JOIN outcome_table o ON f.rinpersoon = o.rinpersoon
    """, [list(outcome_rins_1), list(final_year_rins)]).fetchall()

    outcome_dict = dict(outcome_dict)

    # Clean up temporary tables
    conn.execute("""
        DROP TABLE IF EXISTS synth_hh;
        DROP TABLE IF EXISTS train_hhs;
        DROP TABLE IF EXISTS test_hhs;
    """)

    conn.close()
        
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

    # close all DB connections in conn_dict
    for conn in conn_dict.values():
        conn.close()

    print("All Books of Life with outcomes have been generated and saved in JSONL shards.")

    # Generate token length statistics
    print("\nGenerating token length statistics for the generated Books of Life:")
    generate_token_length_stats(base_dir, sample_size=10000, save_to_file=save_summary)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--bol_name", type=str, required=True, help="Name of the Book of Life data repository that is stored.")
    args.add_argument("--recipe_name", type=str, required=True, help="Name of the recipe file to use. This should be stored in the recipe directory.")
    args.add_argument("--max_processes", type=int, default=4, choices=list(range(1,13)), help="Maximum number of processes to use for parallel generation.")
    args.add_argument("--shard_size", type=int, default=10000, help="Number of entries per shard.")
    args.add_argument("--output_dir", type=str, default=None, help="Output directory to save the data directory.")
    args.add_argument("--save_summary", action='store_true', help="Whether to save the token length statistics summary to the data directory after generation.")
    args = args.parse_args()

    start_time = time.time()
    main(**vars(args))
    print(f"Execution time: {round((time.time() - start_time)/60, 2)} mins.")