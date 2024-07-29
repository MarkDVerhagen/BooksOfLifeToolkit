from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding


model = AutoModelForSequenceClassification.from_pretrained("/scratch/gpfs/vs3041/prefer_prepare/hf_pipeline_MWE/hf_models/Meta-Llama-3-8B", 
                                                           device_map="auto", num_labels = 4)


print(model.config.id2label)