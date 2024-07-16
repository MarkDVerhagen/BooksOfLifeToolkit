#!/bin/bash

module purge

cd $file_path

module load anaconda3/2024.2

# starting environment from scratch
conda remove --name clean_environment --all
echo y

conda create --name clean_environment python=3.7
echo y

# loading torchtune and requirements 
rm -rf $file_path/torchtune 
git clone https://github.com/pytorch/torchtune.git
cd torchtune
pip install -e .





