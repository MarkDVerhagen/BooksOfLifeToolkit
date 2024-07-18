export project_path=$(pwd)

# setting up the environment
module purge
cd $project_path
module load anaconda3/2024.2
conda activate hf_environment

python scripts/evaluation_with_hf.py \
--model_name "llama3-8b" \
--dataset "salganik" \
--fine_tune_method "lora" \
--GPU_util "single" \
--params "default" \
--training_folds "1-2" \
--test_folds "3-3"
