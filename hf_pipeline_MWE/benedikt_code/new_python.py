# arguments from the command line 
parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, help="model name")
parser.add_argument("--dataset", type=str)
parser.add_argument("--fine_tune_method", type=str)
parser.add_argument("--GPU_util", type=str)
parser.add_argument("--params", type=str)
args = parser.parse_args()

model_name = args.model_name
dataset = args.dataset
fine_tune_method = args.fine_tune_method
GPU_util = args.GPU_util

params = args.params

fine_tuned_model_name = "-".join([model_name, dataset, fine_tune_method, GPU_util, params])

if model_name == "llama3-8b":
    model_to_read = project_directory + "/hf_models" + "Meta-Llama-3-8B"
else: 
    raise Exception("Either the model is the wrong place, or we haven't downloaded it yet :(")

if dataset == "n_30k":
    data_to_read = project_directory + "data/fine_tuning_hf/data/fake_data_for_tuning_3cols.csv"
elif dataset == "n_100":
    data_to_read = project_directory + "data/fine_tuning_hf/data/fake_data_for_tuning_3cols_subset.csv"
else:
    raise Exception("Dataset not recognised")

if fine_tune_method == "full":
    pass
else: 
    raise Exception("Haven't written code to support other fine-tune methods yet")

if GPU_util == "single":
    pass
else: 
    raise Exception("Haven't written code to support distributed GPU utilization yet")

# need to insert PEFT and Lora erc. 


import wandb
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset, load_from_disk
from trl import SFTTrainer
from peft import get_peft_model, LoraConfig, AutoPeftModelForSequenceClassification
import argparse
import pandas as pd 


# setting wandb to offline
wandb.init(mode="disabled")   

# model arguments from the command line
parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, help="model name")
args = parser.parse_args()

model_name = args.model_name
ft_name = model_name + "fine-tuned"

project_directory = "/scratch/gpfs/vs3041/fine_tuning_hf/"
training_data_location = project_directory + "data/fine_tuning_hf/data/fake_data_for_tuning_3cols_subset.csv"
output_directory = project_directory + "fine_tuned_models/" + model_name


# reading training data 
train_dataset = pd.read_csv(training_data_location)

# setting up model architecture and initializing tokenizer
model = AutoModelForSequenceClassification.from_pretrained(args.model_name, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(args.model_name)
tokenizer.pad_token = tokenizer.eos_token 

# model hyperparameters
training_args = TrainingArguments(
    output_dir=output_directory,
    logging_steps=20,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=5,
    # weight_decay=0.01,
)

# input padding options 
model.config.pad_token_id = model.config.eos_token_id
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# tokenizing the training data 
def preprocess_function(examples):
    return tokenizer(examples["prompt"], truncation=True)
tokenized_train_data = train_dataset.map(preprocess_function, batched=True)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_data,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train()
trainer.save_model(args.ft_name)