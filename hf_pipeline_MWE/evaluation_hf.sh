export project_path=$(pwd)

# setting up the environment
module purge
cd $project_path
module load anaconda3/2024.2
conda activate hf_environment

python scripts/evaluation_with_hf.py 
