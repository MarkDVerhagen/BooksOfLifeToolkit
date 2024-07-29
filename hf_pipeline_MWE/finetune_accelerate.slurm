#!/bin/bash
#SBATCH --job-name=accelerate    # create a short name for your job
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=8        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=30G                # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:2             # number of gpus per node
#SBATCH --time=12:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=vs3041@princeton.edu
#SBATCH -o output/last_accelerate_run.out # output file 

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
export fine_tune_method="lora"
export GPU_util="single"
export params="default"
export training_folds="0-0"
export test_folds="0-0"

echo "Executing on the machine:" $(hostname)

python scripts/accelerate_example.py 

#accelerate launch --multi_gpu --num_processes 2 scripts/accelerate_example.py 
