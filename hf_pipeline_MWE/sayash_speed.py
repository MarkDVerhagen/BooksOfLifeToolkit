from transformers import AutoTokenizer
import random
import string
from datasets import Dataset
# Load the LLaMA tokenizer
tokenizer = AutoTokenizer.from_pretrained("/scratch/gpfs/vs3041/prefer_prepare/hf_pipeline_MWE/hf_models/Meta-Llama-3.1-8B")
def generate_random_text(num_tokens):
    # Generate a large chunk of random text
    chunk_size = num_tokens * 4  # Estimating 4 characters per token on average
    random_text = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation + ' ', k=chunk_size))
    # Tokenize and truncate to desired length
    tokens = tokenizer.encode(random_text, truncation=False)[:num_tokens]
    # Decode back to text
    return tokenizer.decode(tokens)
def generate_dataset(num_samples, tokens_per_sample):
    data = {
        "text": [],
        "labels": []
    }
    for _ in range(num_samples):
        # Generate random text for text field
        text = generate_random_text(tokens_per_sample)
        # Generate binary label (0 or 1)
        label = random.choice([0, 1])
        data["text"].append(text)
        data["labels"].append(label)
    return Dataset.from_dict(data)
# Generate dataset with 10 samples of 100,000 tokens each
# Adjust these numbers as needed
num_samples = 100
tokens_per_sample = 20000
dataset = generate_dataset(num_samples, tokens_per_sample)
# Save the dataset
dataset.save_to_disk("large_dataset")
print(f"Dataset generated with {num_samples} samples, each containing approximately {tokens_per_sample} tokens.")
print("Dataset saved to 'large_dataset' directory.")
# Display a sample and its token count
print("\nSample entry:")
sample = dataset[0]
print(f"Text (first 100 characters): {sample["text"][:100]}...")
print(f"Label: {sample["labels"]}")
print(f"Actual token count for text: {len(tokenizer.encode(sample["text"]))}")