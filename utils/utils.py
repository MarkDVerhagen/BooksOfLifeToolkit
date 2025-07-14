import tiktoken
from transformers import AutoTokenizer
import numpy as np
import os
import json
import random
from datasets import load_dataset
import duckdb

def generate_token_length_stats(dataset_path: str, sample_size: int = 10000, save_to_file: bool = False):
    # Load the LLaMA 7B tokenizer from the hardcoded local directory
    model_path = "ADD PATH TO LLAMA ON OSSC"
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)

    # tiktoken tokenizer not longer used
    #  tokenizer = tiktoken.encoding_for_model("gpt-4")
    
    dataset = load_dataset(dataset_path)
    
    def get_stats(split):
        book_content = dataset[split]['book_content']
        if len(book_content) > sample_size:
            print(f"Sampling {sample_size} books from {len(book_content)} for the {split} split")
            sampled_content = random.sample(book_content, sample_size)
        else:
            sampled_content = book_content

        lengths = [len(tokenizer.encode(text)) for text in sampled_content]
        return {
            'total_books': len(book_content),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'mean_length': np.mean(lengths),
            'median_length': np.median(lengths),
            'std_length': np.std(lengths)
        }
    
    stats = {split: get_stats(split) for split in dataset.keys()}
    
    # Print statistics
    for split, split_stats in stats.items():
        print(f"\nSummary Statistics for {split} split:")
        for stat, value in split_stats.items():
            if isinstance(value, float):
                print(f"  {stat}: {value:.2f}")
            else:
                print(f"  {stat}: {value}")
    
    if save_to_file:
        with open(os.path.join(dataset_path, 'token_length_stats.json'), 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"\nStatistics saved to {os.path.join(dataset_path, 'token_length_stats.json')}")


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


def save_to_jsonl_shard(data_buffer, output_dir, shard_index):
    """Save a shard of data to a JSONL file."""
    shard_filename = f"shard_{shard_index}.jsonl"
    shard_path = os.path.join(output_dir, shard_filename)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(shard_path, 'a') as jsonl_file:
        for data in data_buffer:
            jsonl_file.write(json.dumps(data) + '\n')


def generate_and_save_book(rinpersoon, db_path, recipe_yaml_path, BookofLifeGenerator=None, conn=None):
    """Generate a Book of Life for a single rinpersoon and include the outcome. Requires BookofLifeGenerator class and a duckdb connection."""
    if BookofLifeGenerator is None or conn is None:
        raise ValueError("BookofLifeGenerator class and duckdb connection must be provided.")
    try:
        generator = BookofLifeGenerator(rinpersoon, recipe_yaml_path=recipe_yaml_path, duck_db_conn=conn)
        book_content = generator.generate_book()
        outcome = None  # Default to None if not found
        return rinpersoon, book_content, outcome
    except Exception as e:
        print(f"Error generating Book of Life for rinpersoon {rinpersoon}: {str(e)}")
        return rinpersoon, None, None


def basic_gen(rinpersoon, recipe_yaml_path, paragraphs, table_version=""):
    generator = BookofLifeGenerator(rinpersoon, recipe_yaml_path, paragraphs, table_version = table_version)
    book_content = generator.generate_book()
    # outcome = outcome_dict.get(rinpersoon, "nan")
    return rinpersoon, book_content #, outcome

def spell_gen(generator, spells=5, include_last_n=None):
    generator.book = ""
    old_pars = generator.paragraphs
    pars = generator.sort_paragraphs('year_dataset_name')
    n_pars = len(pars)

    if include_last_n:
        spells += include_last_n
    generator.paragraphs = pars[-spells:]
    book_content = generator.generate_book()
    generator.paragraphs = old_pars
    return book_content

def save_to_jsonl_shard(data_buffer, output_dir, shard_index):
    """Save a shard of data to a JSONL file."""
    shard_filename = f"shard_{shard_index}.jsonl"
    shard_path = os.path.join(output_dir, shard_filename)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(shard_path, 'a') as jsonl_file:
        for data in data_buffer:
            jsonl_file.write(json.dumps(data) + '\n')