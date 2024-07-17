import wandb
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset, load_from_disk, Dataset
from trl import SFTTrainer
from peft import get_peft_model, LoraConfig, AutoPeftModelForSequenceClassification
import argparse
import pandas as pd 
import time

# setting wandb to offline
wandb.init(mode="offline")   

def format_salganik_data(data):

    ## Taking csv and turning it into HF format

    # HF needs a specific form for the dataset
    data["text"] = data["input"]
    data["labels"] = data["output"]

    # keeping only inputs and outputs
    data = data[["text", "labels"]]

    # making sure outputs are 0s and 1s (will need to make this programatic)
    data["labels"] = (data["labels"] == "kid: 1").astype(int)  

    # converting to HF format
    data = Dataset.from_pandas(data)

    return data

def tokenize_and_prepare(data):

    # Tokenizer for HF models

    return tokenizer(data["text"], truncation=True, padding="max_length", max_length=512)

# model arguments from the command line
parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, help="model name")
parser.add_argument("--dataset", type=str)
parser.add_argument("--fine_tune_method", type=str)
parser.add_argument("--GPU_util", type=str)
parser.add_argument("--params", type=str)
parser.add_argument("--training_folds")
args = parser.parse_args()

model_name = args.model_name
dataset = args.dataset
fine_tune_method = args.fine_tune_method
GPU_util = args.GPU_util
params = args.params
training_folds = args.training_folds
first_training_fold, last_training_fold = map(int, training_folds.split("-"))

project_directory = os.environ.get('project_path') + "/"

fine_tuned_model_name = "-".join([model_name, dataset, fine_tune_method, GPU_util, params, "folds", training_folds])
output_directory = project_directory + "fine_tuned_models/" + fine_tuned_model_name

#### SPECIFIYING MODEL

if model_name == "llama3-8b":
    model_to_read = project_directory + "hf_models/" + "Meta-Llama-3-8B/"
else: 
    raise Exception("Either the model is the wrong place, or we haven't downloaded it yet :(")


#### SPECIFIYING DATA

if dataset == "salganik":
    # reading training data 
    data_to_read = project_directory + "data/salganik_data.csv"
    train_dataset = pd.read_csv(data_to_read)

    # subsetting data to specified training folds 
    train_dataset = train_dataset[train_dataset['fold'].between(first_training_fold, last_training_fold)]

    # formatting the salganik data to get it into a format readable by the LLM
    train_dataset = format_salganik_data(train_dataset)    

else:
    raise Exception("Dataset not recognised")

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

# setting up model architecture and initializing tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_to_read, num_labels=2)
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
else:
    pass


# see: https://huggingface.co/docs/transformers/en/perf_train_gpu_one#batch-size-choice

# model hyperparameters
training_args = TrainingArguments(
    output_dir=output_directory,
    logging_steps=20,
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    num_train_epochs=2,
    gradient_accumulation_steps=4, # improves memory utilization
    # weight_decay=0.01,
)

# input padding options 
model.config.pad_token_id = model.config.eos_token_id
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# tokenizing the training data 
tokenized_train_data = train_dataset.map(tokenize_and_prepare, batched=True)


trainer = Trainer(
    model=model,
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
if fine_tune_method == "lora":
    peft_model.save_pretrained(output_directory)
else:
    trainer.save_pretrained(output_directory)

# saving tokenizer
tokenizer.save_pretrained(output_directory)