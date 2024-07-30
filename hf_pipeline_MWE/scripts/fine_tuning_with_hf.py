import wandb
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset, load_from_disk, Dataset
from trl import SFTTrainer
from peft import get_peft_model, LoraConfig, AutoPeftModelForSequenceClassification
import argparse
import pandas as pd 
import time
import glob
import torch
from data_formatting import get_data

# setting wandb to offline
wandb.init(mode="offline")   


def tokenize_and_prepare(data):

    # Tokenizer for HF models

    return tokenizer(data["text"], truncation=True, padding="max_length", max_length=512)

# model arguments from the command line

model_name = os.environ.get('model_name')
dataset = os.environ.get('dataset')
fine_tune_method = os.environ.get('fine_tune_method')
GPU_util = os.environ.get('GPU_util')
params = os.environ.get('params')
training_folds = os.environ.get('training_folds')
first_training_fold, last_training_fold = map(int, training_folds.split("-"))

project_directory = os.environ.get('project_path') + "/"

fine_tuned_model_name = "-".join([model_name, dataset, fine_tune_method, GPU_util, params, "folds", training_folds])
output_directory = project_directory + "fine_tuned_models/" + fine_tuned_model_name

#### SPECIFIYING MODEL

if model_name == "llama3-8b":
    model_to_read = project_directory + "hf_models/" + "Meta-Llama-3-8B/"
elif model_name == "llama3.1-8b":
    model_to_read = project_directory + "hf_models/" + "Meta-Llama-3.1-8B/"
else: 
    raise Exception("Either the model is the wrong place, or we haven't downloaded it yet :(")


#### SPECIFIYING DATA
train_dataset,_ = get_data(dataset)

#### SPECIFIYING FINE-TUNING METHOD

if fine_tune_method == "full":
    pass
elif fine_tune_method == "lora":
    pass
else: 
    raise Exception("Haven't written code to support other fine-tune methods yet")

#### SPECIFIYING GPU UTILIZATION

if GPU_util == "single":
    pass
else: 
    raise Exception("Haven't written code to support distributed GPU utilization yet")

#### ADDING CUSTOM HYPERPARAMETERS

if params == "default":
    pass
else: 
    raise Exception("Haven't written code to change parameters yet")


# might help with CUDA issues: https://blog.gopenai.com/how-to-resolve-runtimeerror-cuda-out-of-memory-d48995452a0
torch.cuda.empty_cache()


# setting up model architecture and initializing tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_to_read, device_map = "auto")  # num_labels=2,
tokenizer = AutoTokenizer.from_pretrained(model_to_read)
tokenizer.pad_token = tokenizer.eos_token 

if fine_tune_method == "lora":
    peft_config = LoraConfig(task_type="SEQ_CLS", 
                         inference_mode=False, 
                         r=32, 
                         lora_alpha=16, 
                         lora_dropout=0.1)
    peft_model = get_peft_model(model, peft_config)
    print('PEFT Model')
    peft_model.print_trainable_parameters()
    model_to_use = peft_model
else:
    model_to_use = model


# see: https://huggingface.co/docs/transformers/en/perf_train_gpu_one#batch-size-choice

# model hyperparameters
training_args = TrainingArguments(
    output_dir=output_directory,
    logging_steps=10,
    learning_rate=1e-3,
    per_device_train_batch_size=128,
    num_train_epochs=1,
    gradient_accumulation_steps=8, # improves memory utilization
    # weight_decay=0.01
    fp16=True,
    gradient_checkpointing=True,
    save_strategy = "no",  # will save model manually usuing,
    lr_scheduler_type = "cosine",
    warmup_ratio = 0.1 
)

# input padding options 
model_to_use.config.pad_token_id = model_to_use.config.eos_token_id
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# tokenizing the training data 
tokenized_train_data = train_dataset.map(tokenize_and_prepare, batched=True)


trainer = Trainer(
    model=model_to_use,
    args=training_args,
    train_dataset=tokenized_train_data,
    tokenizer=tokenizer,
    data_collator=data_collator,
)


start_time = time.time()

trainer.train()

end_time = time.time()

execution_time = end_time - start_time

print(f"Fine-tuning time: {execution_time} seconds")

# saving model weights
trainer.save_model(output_directory)

# saving tokenizer
tokenizer.save_pretrained(output_directory)