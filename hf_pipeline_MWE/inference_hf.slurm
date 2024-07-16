#!/bin/bash
#SBATCH --job-name=inference     # create a short name for your job
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=8        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=30G         # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=12:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=vs3041@princeton.edu
#SBATCH -o output/last_inference_run.out # output file 

export file_path="/scratch/gpfs/vs3041/fine_tuning_hf/"

mkdir -p $file_path/output/predictions/

# setting up the environment
module purge
cd $file_path 
module load anaconda3/2024.2
conda activate hf_environment

python scripts/inference_with_hf.py \
--model_name "llama3-8b" \
--test_dataset "n_100" \
--fine_tune_method "lora" \
--GPU_util "single" \
--params "default"
