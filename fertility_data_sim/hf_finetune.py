# This example is a very quick showcase of partial fine-tuning the Llama 3.1 8B model

import torch
from datasets import load_dataset

from trl import SFTTrainer
from peft import LoraConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments

model_path = "/scratch/gpfs/mjs3/Meta-Llama-3-8B-Instruct"

model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

pipeline = transformers.pipeline(
    "text-generation",
    model=model_path,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

