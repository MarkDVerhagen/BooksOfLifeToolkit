import os
import glob
from datasets import load_dataset, load_from_disk, Dataset




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

data_dict = format_BOL_data("/scratch/gpfs/vs3041/prefer_prepare/synth/data/e2e/test_template1/train/")

dataset = Dataset.from_list(data_dict)

print(len(dataset["unique_id"]))

