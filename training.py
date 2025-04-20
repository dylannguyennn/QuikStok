from datasets import load_dataset, ClassLabel, DatasetDict
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
import numpy as np
import evaluate

# Load Financial Phrasebank dataset
raw = load_dataset("financial_phrasebank", "sentences_allagree")
# label_names = ["negative", "neutral", "positive"]

# def preprocess(example):
#     return {"text": example["sentence"], "label": label_names.index(example["label"])}

ds = raw["train"].train_test_split(test_size=0.1)
tokenizer = RobertaTokenizerFast.from_pretrained("roberta-base")
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=raw["train"].features["label"].num_classes)

# Tokenization
def tokenize(example):
    return tokenizer(example["sentence"], truncation=True)

ds = ds.map(tokenize, batched=True)
data_collator = DataCollatorWithPadding(tokenizer)
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return accuracy.compute(predictions=preds, references=labels)

# Training
training_args = TrainingArguments(
    output_dir="fin_roberta",
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=16, 
    per_device_eval_batch_size=32,
    num_train_epochs=10, 
    save_total_limit=2,
    load_best_model_at_end=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=ds["train"],
    eval_dataset=ds["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

trainer.train()
trainer.save_model("fin_roberta")


