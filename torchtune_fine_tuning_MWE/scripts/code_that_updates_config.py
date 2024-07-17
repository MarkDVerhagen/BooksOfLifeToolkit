
import yaml
import os

# PIPELINE:
#   1. read relevant torchtune docs into necessary folders 
#   2. make changes where necessary     

# reading from slurm script
model_class = os.environ.get("model_class")
dataset = os.environ.get("dataset")
fine_tune_method = os.environ.get("fine_tune_method")
params = os.environ.get("params")
GPU_utilization = os.environ.get("GPU_utilization")
file_path = os.environ.get("file_path")

file_path = file_path + "/"


elements_of_yaml_changed = dict(model_class=model_class, 
                                dataset=dataset, 
                                fine_tune_method=fine_tune_method,
                                params=params,
                                GPU_utilization=GPU_utilization)

# these parameters determine how to read default configs 

# Step 1: pulling in cofig from torchtune to write over the top of 

# run tune ls 
# basically, we want to copy the config file from tune and then write on top of it
# so, you will want to 

config_path = file_path + "configs/"

if model_class == "llama2" and  fine_tune_method == "lora" and GPU_utilization == "single":
    config_to_pull_from_torchtune  = config_path + "temp/llama2/7B_lora_single_device.yaml"
    config_to_update = config_path + "updated/llama2/" + ",".join([model_class, dataset, fine_tune_method, GPU_utilization, params])


if model_class == "llama3" and  fine_tune_method == "lora" and GPU_utilization == "single":
    config_to_pull_from_torchtune  = config_path + "temp/llama3/8B_lora_single_device.yaml"
    config_to_update = config_path + "updated/llama3/" + ",".join([model_class, dataset, fine_tune_method, GPU_utilization, params])


# Specifiying model 

if model_class == "llama2":

    # these components are native to torchtune 
    model_component = "torchtune.models.llama2.lora_llama2_7b"  
    tokenizer_component =  "torchtune.models.llama2.llama2_tokenizer"

    model_path = file_path + "hf_models/llama2-7b-hf/"

    # these should be located in the model files from github
    tokenizer_path = model_path + "tokenizer.model"

    # might also be in .bin or .safetensor type
    checkpoint_files = [
        "pytorch_model-00001-of-00002.bin",
        "pytorch_model-00002-of-00002.bin"
    ]
    # where to save model weights 
    output_dir = file_path + "fine_tuned_models/llama2-7b-hf-fine-tuned"
    model_type = "LLAMA2"


if model_class == "llama3":

    # these components are native to torchtune 
    model_component = "torchtune.models.llama3.lora_llama3_8b"  
    tokenizer_component =  "torchtune.models.llama3.llama3_tokenizer"

    model_path = file_path + "hf_models/llama3-8b/original/"

    # these should be located in the model files from github
    tokenizer_path = model_path + "tokenizer.model"

    # might also be in .bin or .safetensor type
    checkpoint_files = [
        "consolidated.00.pth",
    ]

    # where to save model weights 
    output_dir = file_path + "fine_tuned_models/llama3-8b-fine-tuned/"
    model_type = "LLAMA3"

# Specifiying dataset

if dataset == "full":
    data_files = file_path + "data/fake_data_for_tuning_3cols.csv"

if dataset == "subset":
    data_files = file_path + "data/fake_data_for_tuning_3cols_subset.csv"

# updating parameters, if necessary. Begin with default where we change nothing
if params == "default":
    pass

# updating model and dataset 

print(config_to_pull_from_torchtune)

with open(config_to_pull_from_torchtune, 'r') as f:

    print("Checking .yaml is not empty...")
    # checking the .yaml is not empty 
    if (os.path.getsize(config_to_pull_from_torchtune) > 0):
        print("File is not empty")
    else:
        print("File is empty")

    # reading in the original file 
    file_with_changes = yaml.safe_load(f)

    # making changes to the yaml

    # model
    file_with_changes['model']['_component_'] = model_component

    # tokenizer
    file_with_changes['tokenizer']['_component_'] = tokenizer_component
    file_with_changes['tokenizer']['path'] = tokenizer_path

    # the dataset key is a little difficult to deal with, so it is 
    # best to delete it altogether and just write it from scratch
    del file_with_changes['dataset']

    file_with_changes["dataset"] = {
        'data_files': data_files,
        'source': "csv",                                     # note that these don't change
        'template': "torchtune.data.AlpacaInstructTemplate",
        '_component_': "torchtune.datasets.instruct_dataset",
        'train_on_input': True,
        'split': "train"
    }

    # checkpoints
    file_with_changes['checkpointer']['checkpoint_dir'] = model_path
    file_with_changes['checkpointer']['checkpoint_files'] = checkpoint_files
    file_with_changes['checkpointer']['output_dir'] = output_dir
    file_with_changes['checkpointer']['model_type'] = model_type

    separator = "-"
    new_config_name = separator.join([model_class, dataset, fine_tune_method, GPU_utilization, params])

    # adding weights and biases logging 
    file_with_changes['metric_logger'] = {
        '_component_': "torchtune.utils.metric_logging.WandBLogger",
        'project': new_config_name,
        'mode': "offline"   # making offline
    }

with open(file_path + 'configs/updated/' + model_class + "/" + new_config_name + ".yaml", 'w') as file:
    yaml.dump(file_with_changes, file)


print("New file written at:" + file_path + 'configs/updated/' + model_class + "/" + new_config_name + ".yaml")
print("These are the changes:")
print(elements_of_yaml_changed)