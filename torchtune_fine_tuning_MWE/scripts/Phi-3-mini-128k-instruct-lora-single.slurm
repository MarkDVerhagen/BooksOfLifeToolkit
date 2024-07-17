#!/bin/bash
#SBATCH --job-name=phi3-single         # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=8        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=64G                # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=12:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=vs3041@princeton.edu
#SBATCH -o output/Phi3-4k-mini-instruct-lora-single.out # output file 

cd scratch/gpfs/vs3041/fine_tuning
module load anaconda3/2024.2
conda activate prefer

tune run recipes/lora_finetune_single_device.py \
--config configs/Phi3-4k-mini-lora-single-device.yaml