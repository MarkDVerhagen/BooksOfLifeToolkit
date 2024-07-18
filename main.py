import sqlite3
import multiprocessing
import pandas as pd
import random
import os
from serialization.BookofLifeGenerator import BookofLifeGenerator
import time
import traceback

def get_unique_rinpersoons(db_path):
    """Fetch all unique rinpersoon IDs from the persoon_tab table."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT rinpersoon FROM persoon_tab")
            rinpersoons = [row[0] for row in cursor.fetchall()]
        return rinpersoons
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def generate_and_save_book(rinpersoon, recipe_yaml_path, output_dir):
    """Generate a Book of Life for a single rinpersoon and save it to a file."""
    try:
        generator = BookofLifeGenerator(rinpersoon, recipe_yaml_path=recipe_yaml_path)
        book_content = generator.generate_book()
        
        filename = f"{rinpersoon}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as file:
            file.write(book_content)
        
    except Exception as e:
        print(f"Error generating Book of Life for rinpersoon {rinpersoon}: {str(e)}")
        print(traceback.format_exc())

def main(max_processes=None):
    # Print number of unique rinpersoons
    db_path = 'synthetic_data.db'
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
    test_rins = list(synth_hh['rinpersoon'][~synth_hh['HOUSEKEEPING_NR'].isin(train_hhs)])
    train_rins = [i for i in train_rins if i in final_year_rins]
    test_rins = [i for i in test_rins if i in final_year_rins]
    
    recipes = ['test_template1', 'test_template2']
    
    num_processes = min(max_processes or multiprocessing.cpu_count(), multiprocessing.cpu_count())
    print(f"Using {num_processes} processes for parallel generation.")
    
    for recipe in recipes:
        recipe_yaml_path = f'./recipes/{recipe}.yaml'
        
        # Generate and save Books of Life
        train_output_dir = os.path.join('synth', 'data', 'e2e', recipe, 'train', 'bol')
        test_output_dir = os.path.join('synth', 'data', 'e2e', recipe, 'test', 'bol')
        os.makedirs(train_output_dir, exist_ok=True)
        os.makedirs(test_output_dir, exist_ok=True)
        
        with multiprocessing.Pool(processes=num_processes) as pool:
            pool.starmap(generate_and_save_book, [(rin, recipe_yaml_path, train_output_dir) for rin in train_rins])
            pool.starmap(generate_and_save_book, [(rin, recipe_yaml_path, test_output_dir) for rin in test_rins])
        
        # Process outcomes
        outcome = pd.read_csv(os.path.join('synth', 'data', 'edit', 'household_bus.csv'))
        outcome = outcome[outcome['DATE_STIRTHH'] == '1999-01-01']
        outcome_rins_1 = outcome['rinpersoon'][outcome['EVENT'] == 'child_born']
        
        train_outcome = ["1" if rin in outcome_rins_1.values else "0" for rin in train_rins]
        test_outcome = ["1" if rin in outcome_rins_1.values else "0" for rin in test_rins]
        
        # Save outcomes
        train_outcome_dir = os.path.join('synth', 'data', 'e2e', recipe, 'train', 'outcome')
        test_outcome_dir = os.path.join('synth', 'data', 'e2e', recipe, 'test', 'outcome')
        os.makedirs(train_outcome_dir, exist_ok=True)
        os.makedirs(test_outcome_dir, exist_ok=True)
        
        for outcome, rin in zip(train_outcome, train_rins):
            with open(os.path.join(train_outcome_dir, f"{rin}.txt"), 'w') as file:
                file.write(outcome)
        
        for outcome, rin in zip(test_outcome, test_rins):
            with open(os.path.join(test_outcome_dir, f"{rin}.txt"), 'w') as file:
                file.write(outcome)
    
    print("All Books of Life and outcomes have been generated and saved.")

if __name__ == "__main__":
    start_time = time.time()
    main(max_processes=4)
    print(f"Execution time: {time.time() - start_time} seconds.")