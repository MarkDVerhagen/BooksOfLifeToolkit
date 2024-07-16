LAST UPDATE: 16 July 2024

# Step 1: Downloading models from HuggingFace

You will need to copy model weights into the `hf_models` directory. The way to do this is to go to the appropriate page on HuggingFace, get permission, and then clone the repository. 

The way to do this for Llama-3 is to:

1. Go to https://huggingface.co/meta-llama/Meta-Llama-3-8B?clone=true and then apply for permission (it should come back fairly quickly)
2. Run `git clone https://huggingface.co/meta-llama/Meta-Llama-3-8B`
3. Notice that the model weights and tokenizer live in the Meta-Llama-3-8B/original.

It is important that you download these models into your scratch directory because there is not enough space in your home directory to hold these files. I can access my scratch directory by using: `cd /scratch/gpfs/vs3041/`

You will need your HuggingFace username and token to complete this step. You can obtain the token from: https://huggingface.co/settings/tokens

# Step 2: create environment named hf_environment

You will need to create a conda environment on Della named hf_environment that contains the packages listed in hf_environment_reqs.txt. The best way to do this is to run:

`conda create --name hf_environment python=3.12`

`pip install -r requirements.txt`

# Step 3: Personalizing slurm jobs

Make sure that you change your the file paths and the email that will receieve updates when the job is completed.

# Step 4: Fine-tuning

Once you are set up, you can run the fine tuning script. You can execute it on Della using `sbatch finetune_hf.slurm`. This will produce an output file (which can be used for debugging and checking logs) in the `output` directory. It will save the fine-tuned weights in a folder called `fine_tuned_models`.

# Step 5: Inference

Now, you can run `sbatch inference_hf.slurm` to generate predictions which will be saved in `output/predictions`. 