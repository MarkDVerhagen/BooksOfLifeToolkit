import os
os.environ['HF_HOME'] = "_cache"
# set wandb mode to offline
import wandb
wandb.init(mode="disabled")
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset, load_from_disk
from trl import SFTTrainer
from peft import get_peft_model, LoraConfig


train_dataset = load_from_disk("/scratch/gpfs/bs6865/gpt-neox/PreFer_train_data_split_train_finetune")
test_dataset = load_from_disk("/scratch/gpfs/bs6865/gpt-neox/PreFer_train_data_split_test_finetune")

model = AutoModelForSequenceClassification.from_pretrained("NousResearch/Meta-Llama-3-8B", num_labels=2)
tokenizer = AutoTokenizer.from_pretrained("NousResearch/Meta-Llama-3-8B")
peft_config = LoraConfig(task_type="SEQ_CLS", 
                         inference_mode=False, 
                         r=32, 
                         lora_alpha=16, 
                         lora_dropout=0.1)
peft_model = get_peft_model(model, peft_config)
print('PEFT Model')
peft_model.print_trainable_parameters()

tokenizer.pad_token = tokenizer.eos_token 



from transformers import AutoModelForSequenceClassification, AutoTokenizer
from datasets import load_dataset
from transformers import Trainer, TrainingArguments
from transformers import DataCollatorWithPadding

model.config.pad_token_id = model.config.eos_token_id

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

def preprocess_function(examples):
    return tokenizer(examples["prompt"], truncation=True)

tokenized_train_data = train_dataset.map(preprocess_function, batched=True)

training_args = TrainingArguments(
    output_dir="./finetuned_models",
    logging_steps=20,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=5,
    # weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_data,
    tokenizer=tokenizer,
    data_collator=data_collator,
    # pass the config to the trainer
    
)

trainer.train()


peft_model.save_pretrained("ft_l3_8b_5epochs")
tokenizer.save_pretrained("ft_l3_8b_5epochs")



from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification
from peft import AutoPeftModelForSequenceClassification

# Assume the model has been saved after training
model_path = "ft_l3_8b_5epochs"

model = AutoPeftModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token



from transformers import pipeline
from tqdm import tqdm

# Create a pipeline for sequence classification
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
# # Example input text
# text = train_dataset[53]['prompt']
# # Make predictions
# predictions = classifier(text)
# # Print the predicted class and score
# predicted_class = predictions[0]['label']
# predicted_score = predictions[0]['score']
# print("Predicted class:", predicted_class)
# print("Predicted score:", predicted_score)


# Evaluate the model on the test set using the pipeline
test_predictions = []
for sample in tqdm(test_dataset):
    prediction = classifier(sample['prompt'])
    print(sample['prompt'])
    print(prediction)
    test_predictions.append(prediction)



# compute accuracy, precision, recall, and F1 score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Extract the true labels from the test set
true_labels = test_dataset['label']
predictions = [pred[0]['label'] for pred in test_predictions]
predictions = [0 if pred == 'LABEL_0' else 1 for pred in predictions]

# Compute the evaluation metrics
accuracy = accuracy_score(true_labels, predictions)
precision = precision_score(true_labels, predictions)
recall = recall_score(true_labels, predictions)
f1 = f1_score(true_labels, predictions)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 score:", f1)

# compute AUC
from sklearn.metrics import roc_auc_score

# Extract the predicted probabilities for the positive class
probabilities = [pred[0]['score'] for pred in test_predictions]

# Compute the AUC
auc = roc_auc_score(true_labels, probabilities)
print("AUC:", auc)