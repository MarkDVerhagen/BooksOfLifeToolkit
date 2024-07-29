#!/bin/bash
module purge
export project_path=$(pwd)

mkdir -p $project_path/output/predictions/

# setting up the environment
cd $project_path 
module load anaconda3/2024.2
conda activate hf_environment

# model options
export model_name="llama3-8b"
export dataset="bol-temp-1"
export fine_tune_method="full"
export GPU_util="single"
export params="default"
export training_folds="0-0"
export test_folds="0-0"

echo "Executing on the machine:" $(hostname)

#python scripts/fine_tuning_with_hf.py 

CUDA_VISIBLE_DEVICES=0 python scripts/fine_tuning_with_hf.py &
CUDA_VISIBLE_DEVICES=1 python scripts/fine_tuning_with_hf.py &
CUDA_VISIBLE_DEVICES=2 python scripts/fine_tuning_with_hf.py &
CUDA_VISIBLE_DEVICES=3 python scripts/fine_tuning_with_hf.py &



