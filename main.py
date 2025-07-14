import os
import duckdb
import json
import argparse
from serialization.instantiator_scripts.persoon_tab import get_person_attributes
from serialization.BookofLifeGeneratorBatch import BookofLifeGeneratorBatch
from utils.utils import get_unique_rinpersoons, save_to_jsonl_shard, basic_gen

def main():
    parser = argparse.ArgumentParser(description="Generate Books of Life from a DuckDB database.")
    parser.add_argument('--db_path', type=str, default="dbs/db.duckdb", help='Path to the DuckDB database file')
    parser.add_argument('--recipe_path', type=str, default="recipes/template.yaml", help='Path to the recipe YAML file')
    parser.add_argument('--output_dir', type=str, default="output", help='Directory to save the output JSONL files')
    parser.add_argument('--shard_index', type=int, default=None, help='Shard index to save the output JSONL files')
    args = parser.parse_args()

    db_path = os.path.join('dbs', args.db_path)
    recipe_path = args.recipe_path + '.yaml'
    output_dir = args.output_dir
    shard_index = args.shard_index

    # Connect to DuckDB
    conn = duckdb.connect(db_path, read_only=True)

    # Get all unique rinpersoon IDs
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
            data = basic_gen(rinpersoon=rinpersoon, recipe_yaml_path=recipe_path, paragraphs=paragraphs)
            json_record = {
                "rinpersoon": data[0],
                "book_content": data[1]
            }
            data_buffer.append(json_record)
            if i % 100 == 0:
                print(f"Processed {i} records...")
        except Exception as e:
            print(f"Error processing rinpersoon {rinpersoon}: {e}")

    save_to_jsonl_shard(data_buffer, output_dir, shard_index)
    print(f"Saved {len(data_buffer)} records to {output_dir}/shard_{shard_index}.jsonl")

if __name__ == "__main__":
    main() 