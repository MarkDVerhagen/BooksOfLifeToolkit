import argparse
import os
import json
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW, get_scheduler
from datasets import load_dataset, Value, Features
from sklearn.metrics import accuracy_score
from tqdm.auto import tqdm
import wandb

def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune LLaMA model for sequence classification.")
    parser.add_argument("--config", type=str, required=True, help="Path to the configuration file.")
    return parser.parse_args()

def main():
    args = parse_args()

    # Initialize distributed training
    local_rank = int(os.environ['LOCAL_RANK'])

    world_size = torch.cuda.device_count()
    print('visible devices', os.environ['CUDA_VISIBLE_DEVICES'])
    print("Rank, worldsize {} {}".format(local_rank, world_size))
    dist.init_process_group("nccl", rank=local_rank, world_size=world_size)
    # dist.init_process_group("nccl")

    # torch.cuda.set_device(local_rank)
    print('j')
    # Load config
    with open(args.config) as f:
        config = json.load(f)

    feature_types = {config['text_column']: Value('string'), config['label_column']: Value('bool')}
    # Load dataset
    dataset = load_dataset("csv", data_files='scripts/parity.csv', features=Features(feature_types))
    dataset = dataset['train'].train_test_split(test_size=.2, seed=42)
    dataset = dataset.map(lambda examples: {'text': examples[config["text_column"]], 'label': examples[config["label_column"]]})

    # Tokenization
    tokenizer = AutoTokenizer.from_pretrained(config["model_name"])      

    def tokenize_function(examples):
        return tokenizer(examples[config["text_column"]], padding='max_length', truncation=True)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    print('a')
    # Prepare Data Loaders
    tokenized_datasets.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])
    train_sampler = DistributedSampler(tokenized_datasets['train'])
    test_sampler = DistributedSampler(tokenized_datasets['test'])
    train_dataloader = DataLoader(tokenized_datasets['train'], sampler=train_sampler, batch_size=config["batch_size"])
    test_dataloader = DataLoader(tokenized_datasets['test'], sampler=test_sampler, batch_size=config["batch_size"])
    print('b')
#     # Load Model
#     if args.qlora:
#         model = load_qlora_model(config["model_name"], config["num_labels"])  # Custom function for QLoRA
#     else:
    model = AutoModelForSequenceClassification.from_pretrained(config["model_name"], num_labels=config["num_labels"])

#     model.to(local_rank)
#     model = DDP(model, device_ids=[local_rank], output_device=local_rank)

#     optimizer = AdamW(model.parameters(), lr=config["learning_rate"])
    
#     if args.num_steps:
#         num_training_steps = args.num_steps
#     else:
#         num_training_steps = config["num_epochs"] * len(train_dataloader)

#     lr_scheduler = get_scheduler(
#         "linear",
#         optimizer=optimizer,
#         num_warmup_steps=0,
#         num_training_steps=num_training_steps
#     )

#     # Training Loop
#     progress_bar = tqdm(range(num_training_steps), disable=local_rank != 0)
#     model.train()

#     for epoch in range(config["num_epochs"]):
#         epoch_loss = 0
#         train_sampler.set_epoch(epoch)
#         for batch in train_dataloader:
#             batch = {k: v.to(local_rank) for k, v in batch.items()}
#             outputs = model(**batch)
#             loss = outputs.loss
#             loss.backward()
#             optimizer.step()
#             lr_scheduler.step()
#             optimizer.zero_grad()
#             progress_bar.update(1)
#             epoch_loss += loss.item()

#             # Log loss to wandb
#             if local_rank == 0:
#                 wandb.log({"train_loss": loss.item()})

#         # Save checkpoint
#         if local_rank == 0 and (epoch + 1) % config["save_checkpoint_every"] == 0:
#             checkpoint_dir = os.path.join(config["output_dir"], f"checkpoint-{epoch + 1}")
#             model.module.save_pretrained(checkpoint_dir)
#             tokenizer.save_pretrained(checkpoint_dir)

#         # Evaluation
#         model.eval()
#         predictions, true_labels = [], []

#         for batch in test_dataloader:
#             batch = {k: v.to(local_rank) for k, v in batch.items()}
#             with torch.no_grad():
#                 outputs = model(**batch)
#             logits = outputs.logits
#             predictions.extend(torch.argmax(logits, dim=-1).cpu().numpy())
#             true_labels.extend(batch['label'].cpu().numpy())

#         accuracy = accuracy_score(true_labels, predictions)
#         if local_rank == 0:
#             wandb.log({"epoch": epoch + 1, "accuracy": accuracy})
#             print(f'Epoch {epoch + 1}: Accuracy: {accuracy}')
#         model.train()

#     # Final model save
#     if local_rank == 0:
#         model.module.save_pretrained(config["output_dir"])
#         tokenizer.save_pretrained(config["output_dir"])

# def load_qlora_model(model_name, num_labels):
#     # Placeholder for loading a model with QLoRA
#     # Replace this with the actual implementation of QLoRA for your model
#     from transformers import AutoModelForSequenceClassification
#     model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
#     # Implement QLoRA-specific modifications here
#     return model

if __name__ == "__main__":
    main()