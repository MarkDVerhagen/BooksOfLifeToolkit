import pandas as pd
import numpy as np
import argparse

def generate_bit_sequences(length, num_sequences, random_parity=False):
    # Generate random bit sequences
    bit_sequences = [''.join(np.random.choice(['0', '1'], length)) for _ in range(num_sequences)]
    
    if random_parity:
        # Generate random bits for the second column
        second_column = np.random.choice(['0', '1'], num_sequences)
    else:
        # Calculate parity for each bit sequence
        second_column = [str(seq.count('1') % 2) for seq in bit_sequences]
    
    # Create DataFrame
    df = pd.DataFrame({'BitSequence': bit_sequences, 'Parity': second_column})
    
    return df

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate bit sequences and their parity/random bit')
    parser.add_argument('--length', type=int, required=True, help='Length of the bit sequences')
    parser.add_argument('--num_sequences', type=int, required=True, help='Number of sequences to generate')
    parser.add_argument('--random_parity', action='store_true', help='Use random bits instead of parity for the second column')
    parser.add_argument('--output', type=str, required=True, help='Output CSV file path')

    # Parse arguments
    args = parser.parse_args()

    # Generate DataFrame
    df = generate_bit_sequences(args.length, args.num_sequences, args.random_parity)
    
    # Save DataFrame to CSV
    df.to_csv(args.output, index=False)
    print(f"DataFrame saved to {args.output}")

if __name__ == "__main__":
    main()