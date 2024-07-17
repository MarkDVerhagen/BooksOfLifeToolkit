import torch
from torch import nn
from torchtune.modules.peft.peft_utils import set_trainable_params
from torchtune.utils import FullModelMetaCheckpointer
from torchtune.models.llama3 import llama3, lora_llama3_8b

from typing import Literal


import json

# 1. Load the trained model
model_directory = "/scratch/gpfs/vs3041/fine_tuning/fine_tuned_models/llama3-8b-fine-tuned/"
checkpoint_file = "meta_model_0.pt"
config_file = "config.json"

#model = config.instantiate(cfg_model)

#model = FullModelMetaCheckpointer()
config = open(model_directory + config_file)

# ["q_proj", "k_proj", "v_proj", "output_proj"]
LORA_ATTN_MODULES = Literal["q_proj", "k_proj", "v_proj", "output_proj"]
# from https://github.com/pytorch/torchtune/blob/bbc48e089b072c7cbaea175bc70501b2193ba482/torchtune/modules/peft/peft_utils.py#L64

#model = lora_llama3_8b(lora_attn_modules = LORA_ATTN_MODULES)

#set_trainable_params(model, config)

model = torch.load(model_directory + checkpoint_file)

print(model)

#model.load_state_dict(torch.load(model_directory + checkpoint_file))
#model.eval()  # Set the model to evaluation mode

# 2. Prepare your input text
#text_to_classify = "Your input text here"

# 3. Preprocess the input (if necessary)
# This step depends on how you preprocessed your training data
# For example, you might need to tokenize the text or convert it to tensors

# 4. Run inference
#with torch.no_grad():
#    output = model(preprocessed_input)