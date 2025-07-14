import os
import duckdb
import json
import argparse
from serialization.BookofLifeGeneratorBatch import BookofLifeGeneratorBatch
from utils.utils import basic_gen

def main():
    parser = argparse.ArgumentParser(description="Inspect the Book of Life for a specific individual.")
    parser.add_argument('--hash', type=str, required=True, help='rinpersoon hash (unique individual ID)')
    parser.add_argument('--recipe', type=str, default="template", help='Recipe YAML file name (without .yaml)')
    parser.add_argument('--db_path', type=str, default="db.duckdb", help='DuckDB database file name (in dbs/)')
    parser.add_argument('--output_dir', type=str, default="output", help='Directory to save the output JSONL file')
    args = parser.parse_args()

    db_path = os.path.join('dbs', args.db_path)
    recipe_path = os.path.join('recipes', args.recipe + '.yaml')
    output_dir = args.output_dir
    rinpersoon = args.hash

    # Connect to DuckDB
    conn = duckdb.connect(db_path, read_only=True)

    # Use the batch generator for a single rinpersoon
    batch_generator = BookofLifeGeneratorBatch([rinpersoon], recipe_path, db_path, conn)
    batch_generator.write_books()
    paragraphs = batch_generator.rin_dicts.get(rinpersoon, [])
    if not paragraphs:
        print(f"No data found for rinpersoon {rinpersoon}.")
        return

    # Generate the Book of Life
    data = basic_gen(rinpersoon=rinpersoon, recipe_yaml_path=recipe_path, paragraphs=paragraphs)
    json_record = {
        "rinpersoon": data[0],
        "book_content": data[1]
    }

    # Print the book content to stdout
    print(f"\nBook of Life for {rinpersoon}:\n{'='*40}\n{json_record['book_content']}\n{'='*40}")

    # Save to JSONL file
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, f"bol_{rinpersoon}.jsonl")
    with open(output_path, 'w') as f:
        f.write(json.dumps(json_record) + '\n')
    print(f"Saved Book of Life to {output_path}")

if __name__ == "__main__":
    main() 