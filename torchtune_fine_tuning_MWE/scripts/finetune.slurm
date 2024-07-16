#!/bin/bash
#SBATCH --job-name=finetuner     # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=8        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=30G                # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=12:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=vs3041@princeton.edu
#SBATCH -o output/last_finetune_run.out # output file 

## Fine tuning parameters

export model_class="llama3"
export dataset="subset"
export fine_tune_method="lora"
export params="default"
export GPU_utilization="single"

## Running bash scripts

export file_path="/scratch/gpfs/vs3041/testing/"

# setting up the environment
module purge
cd $file_path 
module load anaconda3/2024.2
conda activate clean_environment

# NOTE: you will need to get torchtune from GitHub
#bash slurms/create_environment.sh

#conda activate testing

bash slurms/update_config.sh

separator="-"
config_to_call="${model_class}${separator}${dataset}${separator}${fine_tune_method}${separator}${GPU_utilization}${separator}${params}"

# fine-tuning 
tune run "$file_path/recipes/lora_finetune_single_device.py" \
--config "$file_path/configs/updated/$model_class/$config_to_call.yaml"
