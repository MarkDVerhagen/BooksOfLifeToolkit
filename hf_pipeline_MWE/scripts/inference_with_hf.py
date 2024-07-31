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
from data_formatting import get_data

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

def tokenize_and_prepare(data):

    # Tokenizer for HF models

    return tokenizer(data["text"], truncation=True, padding="max_length", max_length=512)


#### SPECIFIYING DATA
_, test_dataset = get_data(dataset)

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
    probability = prediction[0]["score"]

    prediction_probabilities.append(probability)
    prediction_labels.append(label)


save_path = project_directory + "output/predictions/" + model_save_name + "-predictions-" + "folds-" + test_folds + ".csv"

prediction_df = pd.DataFrame({
    #"unique_id": test_dataset["unique_id"], 
    "probabilities": prediction_probabilities,
    "predicted_label": prediction_labels,
    "true_label": test_dataset["labels"]
    })

prediction_df.to_csv(save_path)


