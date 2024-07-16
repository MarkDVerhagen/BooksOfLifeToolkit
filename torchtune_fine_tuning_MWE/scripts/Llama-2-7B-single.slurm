#!/bin/bash
#SBATCH --job-name=llama-2-single         # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=8        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=64G                # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=12:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=vs3041@princeton.edu
#SBATCH -o output/Llama-2-7B-single.out # output file 

# setting up the environment
cd scratch/gpfs/vs3041/fine_tuning
module load anaconda3/2024.2
conda activate prefer

# fine-tuning 
tune run recipes/lora_finetune_single_device.py \
--config configs/updated/llama2/llama2-subset-lora-single-default.yaml