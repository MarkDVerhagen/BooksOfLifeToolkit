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
parser.add_argument("--test_dataset", type=str)
parser.add_argument("--fine_tune_method", type=str)
parser.add_argument("--GPU_util", type=str)
parser.add_argument("--params", type=str)
args = parser.parse_args()

model_name = args.model_name
test_dataset = args.test_dataset
fine_tune_method = args.fine_tune_method
GPU_util = args.GPU_util
params = args.params

project_directory = os.environ.get('project_path') + "/"

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


if test_dataset == "n_30000":
    data_to_read = project_directory + "data/fake_data_for_tuning_3cols.csv"
elif test_dataset == "n_100":
    data_to_read = project_directory + "data/fake_data_for_tuning_3cols_n_100.csv"
elif test_dataset == "n_1000":
    data_to_read = project_directory + "data/fake_data_for_tuning_3cols_subset_n_1000.csv"
elif test_dataset == "n_5000":
    data_to_read = project_directory + "data/fake_data_for_tuning_3cols_subset_n_5000.csv"
elif test_dataset == "n_10000":
    data_to_read = project_directory + "data/fake_data_for_tuning_3cols_subset_n_100000.csv"
elif test_dataset == "n_20000":
    data_to_read = project_directory + "data/fake_data_for_tuning_3cols_subset_n_20000.csv"
else:
    raise Exception("Dataset not recognised")

model_save_name = "-".join([model_name, test_dataset, fine_tune_method, GPU_util, params])

fine_tuned_directory = project_directory + "fine_tuned_models/" + model_save_name

# formatting dataset
test_dataset = pd.read_csv(data_to_read)
test_dataset = format_fake_data(test_dataset)


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

save_path = project_directory + "output/predictions/" + model_save_name + ".csv"
prediction_df = pd.DataFrame(prediction_probabilities)
prediction_df.to_csv(save_path)


