#!/bin/bash
#SBATCH --job-name=llama_finetune
#SBATCH --output=llama_finetune_%j.log
#SBATCH --error=llama_finetune_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=NUM_GPUS_YOU_HAVE
#SBATCH --gres=gpu:NUM_GPUS_YOU_HAVE
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --partition=gpu

# Load necessary modules
module load cuda/11.3
module load anaconda/3
source activate myenv  # Assuming you have a conda environment set up

# Set the number of GPUs
export NUM_GPUS=NUM_GPUS_YOU_HAVE

# Launch the distributed training
srun python -m torch.distributed.launch \
    --nproc_per_node=$NUM_GPUS \
    train_llama_sequence_classification.py \
    --config config.json \
    --model_name "your-model-name" \
    --qlora \
    --learning_rate 3e-5 \
    --num_steps 10000
