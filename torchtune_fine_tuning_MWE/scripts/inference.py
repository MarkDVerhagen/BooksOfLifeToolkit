import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

model_name = 

# Load the model architecture
model = LlamaForCausalLM.from_pretrained("/scratch/gpfs/vs3041/fine_tuning/hf_models/llama3-8b")

# loading the fine-tuned model 
state_dict = torch.load("/scratch/gpfs/vs3041/fine_tuning/fine_tuned_models/llama3-8b-fine-tuned/meta_model_0.pt")
model.load_state_dict(state_dict)

# setting up the tokenizer
tokenizer = LlamaTokenizer.from_pretrained("path/to/original/llama3/tokenizer")
