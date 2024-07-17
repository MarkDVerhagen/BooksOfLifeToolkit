import wandb
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset, load_from_disk, Dataset
from trl import SFTTrainer
from peft import get_peft_model, LoraConfig, AutoPeftModelForSequenceClassification
import argparse
import pandas as pd 
from transformers import pipeline
from tqdm import tqdm

# model arguments from the command line
parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, help="model name")
parser.add_argument("--dataset", type=str)
parser.add_argument("--fine_tune_method", type=str)
parser.add_argument("--GPU_util", type=str)
parser.add_argument("--params", type=str)
parser.add_argument("--training_folds")
parser.add_argument("--test_folds")
args = parser.parse_args()

model_name = args.model_name
dataset = args.dataset
fine_tune_method = args.fine_tune_method
GPU_util = args.GPU_util
params = args.params
training_folds = args.training_folds
first_training_fold, last_training_fold = map(int, training_folds.split("-"))
test_folds = args.test_folds

project_directory = os.environ.get('project_path') + "/"

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


#### SPECIFIYING DATA

if dataset == "salganik":
    # reading training data 
    data_to_read = project_directory + "data/salganik_data.csv"
    test_dataset = pd.read_csv(data_to_read)

    # subsetting data to specified training folds 
    test_dataset = test_dataset[test_dataset['fold'].between(first_test_fold, last_test_fold)]

    # for keeping track of predictions when saving
    index_column = test_dataset["rinpersoon"]

    # formatting the salganik data to get it into a format readable by the LLM
    test_dataset = format_salganik_data(test_dataset)    

else:
    raise Exception("Dataset not recognised")

# path to where the fine-tuned model is saved 
model_save_name = "-".join([model_name, dataset, fine_tune_method, GPU_util, params, "folds", training_folds])
fine_tuned_directory = project_directory + "fine_tuned_models/" + model_save_name

# Load the fine-tuned model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(fine_tuned_directory, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(fine_tuned_directory)
tokenizer.pad_token = tokenizer.eos_token

# Create a pipeline for sequence classification
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Evaluate the model on the test set using the pipeline
prediction_probabilities = []
for sample in tqdm(test_dataset):
    prediction = classifier(sample["text"])

    label = prediction[0]["label"]
    soft_max_probability = prediction[0]["score"]

    prediction_probabilities.append(soft_max_probability)


save_path = project_directory + "output/predictions/" + model_save_name + "-predictions-" + "folds-" + test_folds + ".csv"

prediction_df = pd.DataFrame({
    "rinspersoon": index_column, 
    "softmax_probabilities": prediction_probabilities
    })

prediction_df.to_csv(save_path)


