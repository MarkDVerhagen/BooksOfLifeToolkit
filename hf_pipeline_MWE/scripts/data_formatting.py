# formatting datasets for test runs 

import wandb
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset, load_from_disk, Dataset, Value, Features
from trl import SFTTrainer
from peft import get_peft_model, LoraConfig, AutoPeftModelForSequenceClassification
import argparse
import pandas as pd 
import time
import glob
import torch


# goal is to return a HF Dataset object with "text" and "labels" columns 


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

def extract_unique_id(filename):

    # extract from books of life 
    if "bol/" in filename:
        start = filename.index('bol/') + len('bol/')
        end = filename.index('.txt')

    elif "outcome/" in filename:
        start = filename.index('outcome/') + len('outcome/')
        end = filename.index('.txt')
    else: 
        ValueError("Can't find unique id from filename")
    
    return filename[start:end]

def format_BOL_data(path_to_training_data):
    
    # Step 1: reading in books of life

    # the books of life are contained in multiple .txt files 
    BOL_txt_files = glob.glob(path_to_training_data + "bol/" + '*.txt')

    books_of_life = []
    unique_ids = []
    data = []

    for txt_file in BOL_txt_files:

        #reading books of life
        with open(txt_file, 'r') as infile:
            book_of_life = infile.read().strip()
            unique_id = extract_unique_id(txt_file)     # extract unique_id from filename

        
        # reading outcomes
        outcome_txt_file = path_to_training_data + "outcome/" + unique_id + '.txt'
        with open(outcome_txt_file, 'r') as infile:
            outcome = infile.read().strip()

        data_for_unique_id = {
            "text": book_of_life,
            "unique_id": unique_id,
            "labels": int(outcome)
        }

        data.append(data_for_unique_id)

    data = Dataset.from_list(data)

    return data

def format_juanky_data(path_to_training_data):

    text_column = "BitSequence"
    label_column = "Parity"
    
    dataset = pd.read_csv(path_to_training_data)
    dataset["text"] = dataset["BitSequence"].astype(str)  
    dataset["labels"] = dataset["Parity"].astype(int)  
    #dataset = dataset['train'].train_test_split(test_size=.2, seed=42)

    #data = dataset.map(lambda examples: {'text': examples[text_column], 'label': examples[label_column]})
    data = Dataset.from_pandas(dataset)

    return data 

def get_data(dataset):

    if dataset == "salganik":
        # reading training data 
        data_to_read = project_directory + "data/salganik_data.csv"
        train_dataset = pd.read_csv(data_to_read)

        # formatting the salganik data to get it into a format readable by the LLM
        train_dataset = format_salganik_data(train_dataset)    

        print("Using " + dataset)

        print("samples = " + str(len(train_dataset)))

    elif dataset == "bol-temp-1" or dataset == "bol-temp-2":

        data_to_read =  "/scratch/gpfs/vs3041/prefer_prepare/synth/data/e2e/test_template1/train/"

        train_dataset = format_BOL_data(data_to_read)

        print("Using " + dataset)

        print("samples = " + str(len(train_dataset)))
        
    elif dataset == "juanky_parity":

        data_to_read =  "/scratch/gpfs/vs3041/prefer_prepare/hf_pipeline_MWE/scripts/parity.csv"

        train_dataset = format_juanky_data(data_to_read)

        print("Using " + dataset)

        print("samples = " + str(len(train_dataset)))

    elif dataset == "juanky_random":

        data_to_read =  "/scratch/gpfs/vs3041/prefer_prepare/hf_pipeline_MWE/scripts/random.csv"

        train_dataset = format_juanky_data(data_to_read)

        print("Using" + dataset)

        print("samples = " + str(len(train_dataset)))

    elif dataset == "sayash_speed":

        data_to_read =  "/scratch/gpfs/vs3041/prefer_prepare/hf_pipeline_MWE/large_dataset/"

        train_dataset = load_from_disk(data_to_read)

    else:
        raise Exception("Dataset not recognised")
    
    columns = train_dataset.column_names
    
    if not "labels" in columns and "text" in columns:
        raise Exception("Dataset does not have either text or labels")

    split_dataset = train_dataset.train_test_split(test_size=0.2, seed=42)

    # This creates a DatasetDict with 'train' and 'test' splits
    train_dataset = split_dataset["train"]
    test_dataset = split_dataset["test"]

    

    return train_dataset, test_dataset


