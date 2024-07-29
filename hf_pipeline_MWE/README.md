LAST UPDATE: 16 July 2024

# Step 1: Downloading models from HuggingFace

You will need to copy model weights into the `hf_models` directory. The way to do this is to go to the appropriate page on HuggingFace, get permission, and then clone the repository. 

The way to do this for Llama-3 is to:

1. Go to https://huggingface.co/meta-llama/Meta-Llama-3-8B?clone=true and then apply for permission (it should come back fairly quickly)
2. Run `git clone https://huggingface.co/meta-llama/Meta-Llama-3-8B` 
3. Notice that the model weights and tokenizer live in the Meta-Llama-3-8B/original.

It is important that you download these models into your scratch directory because there is not enough space in your home directory to hold these files. I can access my scratch directory by using: `cd /scratch/gpfs/vs3041/`

You will need your HuggingFace username and token to complete this step. You can obtain the token from: https://huggingface.co/settings/tokens

## Notes from Matt

- What is the best order for this information?  For example, should the information about scratch come before or after the download?

- I think we want Mata-Llama-3-8B-Instruct not Mata-Llama-3-8B

- I was having some trouble with the access token so I switched to this command:
git clone https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct

- Step 2 can take a few minutes, I would recommend adding a note for anything that takes more than a few seconds just so the user understasn it might take some time.

# Step 2: create environment named hf_environment

You will need to create a conda environment on Della named hf_environment that contains the packages listed in hf_environment_reqs.txt. The best way to do this is to run:

`conda create --name hf_environment python=3.12`

`pip install -r requirements.txt`

`conda activate hf_environment`

## Notes from Matt

- I'm curious about conda install vs pip install.  But, if this works I would just leave it.

- I got a few wanrings like this:
WARNING: The script datasets-cli is installed in '/home/mjs3/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

I don't think this is a problem.

- I got this error:
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
conda-repo-cli 1.0.75 requires requests_mock, which is not installed.
mdit-py-plugins 0.3.0 requires markdown-it-py<3.0.0,>=1.0.0, but you have markdown-it-py 3.0.0 which is incompatible.
botocore 1.31.64 requires urllib3<2.1,>=1.25.4; python_version >= "3.10", but you have urllib3 2.2.2 which is incompatible.
s3fs 2023.10.0 requires fsspec==2023.10.0, but you have fsspec 2024.5.0 which is incompatible.
conda-repo-cli 1.0.75 requires clyent==1.2.1, but you have clyent 1.2.2 which is incompatible.
conda-repo-cli 1.0.75 requires python-dateutil==2.8.2, but you have python-dateutil 2.9.0.post0 which is incompatible.
conda-repo-cli 1.0.75 requires requests==2.31.0, but you have requests 2.32.3 which is incompatible.
streamlit 1.30.0 requires packaging<24,>=16.8, but you have packaging 24.1 which is incompatible.
streamlit 1.30.0 requires protobuf<5,>=3.20, but you have protobuf 5.27.2 which is incompatible.

I don't think this is a problem.  Actually this is a problem.
(hf_environment) [mjs3@della-vis1 scripts]$ conda list
# packages in environment at /home/mjs3/.conda/envs/hf_environment:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
bzip2                     1.0.8                h5eee18b_6  
ca-certificates           2024.7.2             h06a4308_0  
expat                     2.6.2                h6a678d5_0  
ld_impl_linux-64          2.38                 h1181459_1  
libffi                    3.4.4                h6a678d5_1  
libgcc-ng                 11.2.0               h1234567_1  
libgomp                   11.2.0               h1234567_1  
libstdcxx-ng              11.2.0               h1234567_1  
libuuid                   1.41.5               h5eee18b_0  
ncurses                   6.4                  h6a678d5_0  
openssl                   3.0.14               h5eee18b_0  
pip                       24.0            py312h06a4308_0  
python                    3.12.4               h5148396_1  
readline                  8.2                  h5eee18b_0  
setuptools                69.5.1          py312h06a4308_0  
sqlite                    3.45.3               h5eee18b_0  
tk                        8.6.14               h39e8969_0  
tzdata                    2024a                h04d1e81_0  
wheel                     0.43.0          py312h06a4308_0  
xz                        5.4.6                h5eee18b_1  
zlib                      1.2.13               h5eee18b_1  

I tried a new way to install.

conda create --name hf python=3.12
conda activate hf
conda install conda-forge::transformers --debug # debug not needed but this takes a long time and it shows what is happening
conda install conda-forge::trl --debug 

# I don't understand why I need to pip install after conda install but OK
pip install transformers -U
pip install wandb

# Step 3: Personalizing slurm jobs

Make sure that you change your the file paths and the email that will receieve updates when the job is completed.

## Notes from matt

- Which files do I need to edit?  I need to edit finetune_hf.slurm.

- Also rather than editing fine_tuning_with_hf.py I moved my directories around a bit.  That way I can pull any changes that you make to that file.



# Step 4: Fine-tuning

Once you are set up, you can run the fine tuning script. You can execute it on Della using `sbatch finetune_hf.slurm`. This will produce an output file (which can be used for debugging and checking logs) in the `output` directory. It will save the fine-tuned weights in a folder called `fine_tuned_models`.

# Step 5: Inference

Now, you can run `sbatch inference_hf.slurm` to generate predictions which will be saved in `output/predictions`. 