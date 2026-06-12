import os
import argparse

import duckdb

from serialization.BookofLifeGeneratorBatch import BookofLifeGeneratorBatch
from utils.utils import get_unique_rinpersoons, save_to_jsonl_shard, basic_gen


def resolve_db_path(db_path):
    """Accept either a full path or a bare filename inside ``dbs/``."""
    return db_path if os.path.exists(db_path) else os.path.join('dbs', db_path)


def resolve_recipe_path(recipe_path):
    """Accept a recipe path with or without the ``.yaml`` extension."""
    return recipe_path if recipe_path.endswith('.yaml') else recipe_path + '.yaml'


def main():
    parser = argparse.ArgumentParser(description="Generate Books of Life from a DuckDB database.")
    parser.add_argument('--db_path', type=str, default="dbs/db.duckdb", help='Path to the DuckDB database file (or a filename inside dbs/)')
    parser.add_argument('--recipe_path', type=str, default="recipes/template.yaml", help='Path to the recipe YAML file (with or without .yaml)')
    parser.add_argument('--output_dir', type=str, default="output", help='Directory to save the output JSONL files')
    parser.add_argument('--shard_index', type=int, default=None, help='Shard index to save the output JSONL files')
    args = parser.parse_args()

    db_path = resolve_db_path(args.db_path)
    recipe_path = resolve_recipe_path(args.recipe_path)
    output_dir = args.output_dir
    shard_index = args.shard_index

    conn = duckdb.connect(db_path, read_only=True)

    rinpersoons = get_unique_rinpersoons(db_path)
    if not rinpersoons:
        print("No rinpersoon IDs found. Exiting.")
        return
    print(f"Found {len(rinpersoons)} unique rinpersoon IDs.")

    # Create batch generator and instantiate paragraphs
    batch_generator = BookofLifeGeneratorBatch(rinpersoons, recipe_path, db_path, conn)
    batch_generator.write_books()

    # Generate books and save to JSONL
    data_buffer = []
    for i, (rinpersoon, paragraphs) in enumerate(batch_generator.rin_dicts.items(), 1):
        try:
            data = basic_gen(rinpersoon=rinpersoon, recipe_yaml_path=recipe_path, paragraphs=paragraphs, conn=conn)
            data_buffer.append({"rinpersoon": data[0], "book_content": data[1]})
            if i % 100 == 0:
                print(f"Processed {i} records...")
        except Exception as e:
            print(f"Error processing rinpersoon {rinpersoon}: {e}")

    shard_path = save_to_jsonl_shard(data_buffer, output_dir, shard_index)
    print(f"Saved {len(data_buffer)} records to {shard_path}")


if __name__ == "__main__":
    main()
