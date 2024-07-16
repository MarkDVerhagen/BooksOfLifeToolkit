#!/bin/bash


# creating necessary folders if they don't exist
mkdir -p "$file_path/configs/temp/$model_class/"
mkdir -p "$file_path/configs/updated/$model_class/"
mkdir -p "$file_path/recipes/"
mkdir -p "$file_path/fine_tuned_models/llama3-8b-fine-tuned/"
mkdir -p "$file_path/fine_tuned_models/llama2-7b-fine-tuned/"


if [ "$model_class" = "llama2" ] && [ "$fine_tune_method" = "lora" ] && [ "$GPU_utilization" = "single" ]; then
    # commands to execute if condition is true
    export config_from_torchtune="llama2/7B_lora_single_device"
    export recipe_from_torchtune="lora_finetune_single_device"

fi

if [ "$model_class" = "llama3" ] && [ "$fine_tune_method" = "lora" ] && [ "$GPU_utilization" = "single" ]; then
    # commands to execute if condition is true
    export config_from_torchtune="llama3/8B_lora_single_device"
    export recipe_from_torchtune="lora_finetune_single_device"
fi

# getting baseline config file
tune cp "$config_from_torchtune" "$file_path/configs/temp/$config_from_torchtune"

tune cp "$recipe_from_torchtune" "$file_path/recipes/$recipe_from_torchtune"

# updating the baseline config file
python "$file_path/slurms/code_that_updates_config.py"

