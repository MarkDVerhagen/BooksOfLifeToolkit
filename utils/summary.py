import tiktoken
import numpy as np
import os
import json
import random
from datasets import load_dataset

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
