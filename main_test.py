import argparse
import os
from serialization.BookofLifeGenerator import BookofLifeGenerator
import duckdb

conn = duckdb.connect("synthetic_data.duckdb", read_only=True)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate Book of Life')
    parser.add_argument('--hash', required=True, help='The hash value for the generator')
    parser.add_argument('--recipe', required=True, help='The recipe file for the generator')
    args = parser.parse_args()

    # Example usage with command-line arguments
    generator = BookofLifeGenerator(args.hash,
                                    os.path.join('recipes', args.recipe + '.yaml'))
    print("Partner:", generator.social_context_paragraphs)
    # Uncomment and replace the below line to use the generate_book method if needed
    # print("Partner's child:", generator.social_context_paragraphs['household_bus']['partners'].social_context_paragraphs['household_bus']['children'].generate_book())
    print('Main book:', generator.generate_book())
    # Uncomment the below line if you need additional prints
    # print("Partner's child:", generator.social_context_paragraphs)

    # Uncomment to print annotations if needed
    # print(generator.paragraphs[0].__annotations__)

if __name__ == "__main__":
    main()
