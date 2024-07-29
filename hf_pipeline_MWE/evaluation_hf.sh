export project_path=$(pwd)

# setting up the environment
module purge
cd $project_path
module load anaconda3/2024.2
conda activate hf_environment

export model_name="llama3-8b"
export dataset="bol-temp-1"
export fine_tune_method="lora"
export GPU_util="single"
export params="default"
export training_folds="0-0"
export test_folds="0-0"

python scripts/evaluation_with_hf.py 
