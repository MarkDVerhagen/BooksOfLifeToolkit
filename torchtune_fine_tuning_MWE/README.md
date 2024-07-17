LAST UPDATE: 10 July 2024

This directory provides a minimum working example for fine-tuning using the `torchtune` package. 

I decided to stop working on this because there was an issue turning the .pt file (which is generated once we fine-tune a model) into a format that could  be used for inference.

I tried to use llama.cpp convert functions to get it into GGUF form which can be used with llama.cpp, but was getting an error: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct/discussions/109 

I tried to do it manually with PyTorch. I ran into issues understanding which model class to initialize the saved weights as.

Some solutions suggested using the transformers package to read in the model to from_pretrained(): https://github.com/huggingface/transformers/issues/30388 

But, in that case it probably just makes sense to go with huggingface. 

You will need to copy over hf_models either from /scratch/gpfs/vs3041, or will need to download the models from github. Make sure that the model names correspond with what is in the code. 

