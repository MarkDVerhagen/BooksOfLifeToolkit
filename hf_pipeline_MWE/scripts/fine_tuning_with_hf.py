import wandb
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset, load_from_disk, Dataset
from trl import SFTTrainer
from peft import get_peft_model, LoraConfig, AutoPeftModelForSequenceClassification
import argparse
import pandas as pd 

# setting wandb to offline
wandb.init(mode="offline")   

# model arguments from the command line
parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, help="model name")
parser.add_argument("--train_dataset", type=str)
parser.add_argument("--fine_tune_method", type=str)
parser.add_argument("--GPU_util", type=str)
parser.add_argument("--params", type=str)
args = parser.parse_args()

model_name = args.model_name
train_dataset = args.train_dataset
fine_tune_method = args.fine_tune_method
GPU_util = args.GPU_util
params = args.params

project_directory = os.environ.get('project_path') + "/"

fine_tuned_model_name = "-".join([model_name, train_dataset, fine_tune_method, GPU_util, params])
output_directory = project_directory + "fine_tuned_models/" + fine_tuned_model_name

if model_name == "llama3-8b":
    model_to_read = project_directory + "hf_models/" + "Meta-Llama-3-8B/"
else: 
    raise Exception("Either the model is the wrong place, or we haven't downloaded it yet :(")

if train_dataset == "n_30k":
    data_to_read = project_directory + "data/fake_data_for_tuning_3cols.csv"
elif train_dataset == "n_100":
    data_to_read = project_directory + "data/fake_data_for_tuning_3cols_subset.csv"
else:
    raise Exception("Dataset not recognised")

if fine_tune_method == "full":
    pass
elif fine_tune_method == "lora":
    pass
else: 
    raise Exception("Haven't written code to support other fine-tune methods yet")

if GPU_util == "single":
    pass
else: 
    raise Exception("Haven't written code to support distributed GPU utilization yet")

if params == "default":
    pass
else: 
    raise Exception("Haven't written code to change parameters yet")

def format_fake_data(data):

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

# reading training data and converting to hugging face format
train_dataset = pd.read_csv(data_to_read)
train_dataset = format_fake_data(train_dataset)

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

# clearing cuda(maybe?)


# model hyperparameters
training_args = TrainingArguments(
    output_dir=output_directory,
    logging_steps=20,
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    num_train_epochs=2,
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

trainer.train()

# saving model weights
if fine_tune_method == "lora":
    peft_model.save_pretrained(output_directory)
else:
    trainer.save_pretrained(output_directory)

# saving tokenizer
tokenizer.save_pretrained(output_directory)