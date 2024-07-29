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
import glob

model_name = os.environ.get('model_name')
dataset = os.environ.get('dataset')
fine_tune_method = os.environ.get('fine_tune_method')
GPU_util = os.environ.get('GPU_util')
params = os.environ.get('params')
training_folds = os.environ.get('training_folds')
test_folds = os.environ.get('test_folds')

first_training_fold, last_training_fold = map(int, training_folds.split("-"))
first_test_fold, last_test_fold = map(int, test_folds.split("-"))

project_directory = os.environ.get('project_path') + "/"

def format_salganik_data(data):

    ## Taking csv and turning it into HF format

    # HF needs a specific form for the dataset
    data["text"] = data["input"]
    data["labels"] = data["output"]

    # keeping only inputs and outputs
    data = data[["text", "labels"]]

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

    # making sure outputs are 0s and 1s (will need to make this programatic)
    test_dataset["output"] = (test_dataset["output"] == "kid: 1").astype(int)  

    # for keeping track of predictions when saving
    index_column = test_dataset["rinpersoon"]
    true_labels = test_dataset["output"]

    # formatting the salganik data to get it into a format readable by the LLM
    test_dataset = format_salganik_data(test_dataset)    

elif dataset == "bol-temp-1":
    data_to_read =  "/scratch/gpfs/vs3041/prefer_prepare/synth/data/e2e/test_template1/test/"  # make sure this is test

    test_dataset = format_BOL_data(data_to_read)

    index_column = test_dataset["unique_id"]

elif dataset == "bol-temp-2":
    data_to_read =  "/scratch/gpfs/vs3041/prefer_prepare/synth/data/e2e/test_template2/test/"  # make sure this is test

    test_dataset = format_BOL_data(data_to_read)

    index_column = test_dataset["unique_id"]


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
prediction_labels = []
for sample in tqdm(test_dataset):
    prediction = classifier(sample["text"])

    label = prediction[0]["label"]
    soft_max_probability = prediction[0]["score"]

    prediction_probabilities.append(soft_max_probability)
    prediction_labels.append(label)


save_path = project_directory + "output/predictions/" + model_save_name + "-predictions-" + "folds-" + test_folds + ".csv"

prediction_df = pd.DataFrame({
    "unique_id": test_dataset["unique_id"], 
    "softmax_probabilities": prediction_probabilities,
    "predicted_label": prediction_labels,
    "true_label": test_dataset["labels"]
    })

prediction_df.to_csv(save_path)


