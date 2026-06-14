import os
import json
import random

import numpy as np
import duckdb

from serialization.BookofLifeGenerator import BookofLifeGenerator


def generate_token_length_stats(dataset_path: str, tokenizer_name_or_path: str,
                                sample_size: int = 10000, save_to_file: bool = False):
    """Summarise the token-length distribution of generated books of life.

    This helper is only needed for the optional downstream fine-tuning workflow,
    so its heavy dependencies (``transformers``/``datasets``/``tiktoken``) are
    imported lazily. Install them with ``pip install bolt[stats]``.

    Parameters
    ----------
    dataset_path : str
        Path or name passed to ``datasets.load_dataset``.
    tokenizer_name_or_path : str
        A Hugging Face tokenizer name or a local path to one.
    sample_size : int, default 10000
        Maximum number of books to sample per split.
    save_to_file : bool, default False
        If True, write the statistics to ``token_length_stats.json``.
    """
    from transformers import AutoTokenizer
    from datasets import load_dataset

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path, use_fast=False)
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
            'std_length': np.std(lengths),
        }

    stats = {split: get_stats(split) for split in dataset.keys()}

    for split, split_stats in stats.items():
        print(f"\nSummary Statistics for {split} split:")
        for stat, value in split_stats.items():
            if isinstance(value, float):
                print(f"  {stat}: {value:.2f}")
            else:
                print(f"  {stat}: {value}")

    if save_to_file:
        out_path = os.path.join(dataset_path, 'token_length_stats.json')
        with open(out_path, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"\nStatistics saved to {out_path}")

    return stats


def get_unique_rinpersoons(db_path):
    """Fetch all unique rinpersoon IDs from the persoon_tab table."""
    conn = duckdb.connect(db_path, read_only=True)
    try:
        table_exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='persoon_tab'"
        ).fetchone()
        if not table_exists:
            print("Table 'persoon_tab' does not exist in the database.")
            return []

        row_count = conn.execute("SELECT COUNT(*) FROM persoon_tab").fetchone()[0]
        print(f"Number of rows in persoon_tab: {row_count}")

        result = conn.execute("SELECT DISTINCT rinpersoon FROM persoon_tab").fetchall()
        return [row[0] for row in result]
    finally:
        conn.close()


def basic_gen(rinpersoon, recipe_yaml_path, paragraphs, table_version="", conn=None):
    """Generate a book from pre-instantiated paragraphs.

    Pass ``conn`` (a DuckDB connection) when the recipe defines social context so
    that nested "books within books" can be written for household members.
    """
    generator = BookofLifeGenerator(
        rinpersoon,
        recipe_yaml_path,
        paragraphs,
        duck_db_conn=conn,
        table_version=table_version,
    )
    book_content = generator.generate_book()
    return rinpersoon, book_content


def save_to_jsonl_shard(data_buffer, output_dir, shard_index=None):
    """Append a buffer of records to a JSONL shard file."""
    shard_filename = f"shard_{shard_index}.jsonl" if shard_index is not None else "books.jsonl"
    shard_path = os.path.join(output_dir, shard_filename)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(shard_path, 'a') as jsonl_file:
        for data in data_buffer:
            jsonl_file.write(json.dumps(data) + '\n')

    return shard_path
