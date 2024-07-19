# writing a function that evalutates predictions over folds 

import pandas as pd
from datetime import datetime
import json
import argparse
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


### I don't need this for now, but I think it might be useful in the future 

def writing_prediction_metadata(training_folds: list,
                                test_folds: list, 
                                model_id: str,
                                comment: str,
                                path_to_text_file):

    # when we are generating predictions in either Stork Oracle or for the 
    # Books of Life, we want to create meta-data for the predicted values:

    # training folds: what data was the model trained on? A list of RINSPERSONS
    # test folds: what data was the model fit on? A list of RINSPERSONS
    # model_id: the model id 
    # comment: user defined comments
    # path_to_text_file: where to save output?

    # Get the current time
    now = datetime.now()

    # Format the time to year, month, day, hour, and minute
    formatted_date_time = now.strftime('%Y-%m-%d---%H-%M-%S')

    metadata = thisdict = {
    "model_id": model_id,
    "date_time": formatted_date_time,
    "training_folds": training_folds,
    "test_folds": test_folds
    }

    with open("metadata.json", "w") as outfile: 
        json.dump(metadata, outfile)


# model arguments from the command line
model_name = os.environ.get('model_name')
dataset = os.environ.get('dataset')
fine_tune_method = os.environ.get('fine_tune_method')
GPU_util = os.environ.get('GPU_util')
params = os.environ.get('params')
training_folds = os.environ.get('training_folds')
test_folds = os.environ.get('test_folds')

# location of project
project_directory = os.environ.get('project_path') + "/"

# model metadata
fine_tuned_model_name = "-".join([model_name, dataset, fine_tune_method, GPU_util, params, "folds", training_folds])

# file with predictions stored
path_to_predictions = project_directory + "output/predictions/" + fine_tuned_model_name + "-predictions-" + "folds-" + test_folds + ".csv"
prediction_data = pd.read_csv(path_to_predictions)

### Formatting for Sklearn

# these are in the form "LABEL_0" and "LABEL_1"
predictions = prediction_data["predicted_label"]
formatted_predictons = [0 if  prediction == 'LABEL_0' else 1 for prediction in predictions]
true_labels = prediction_data["true_label"]

accuracy = accuracy_score(true_labels, formatted_predictons)
precision = precision_score(true_labels, formatted_predictons)
recall = recall_score(true_labels, formatted_predictons)
f1 = f1_score(true_labels, formatted_predictons)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 score:", f1)