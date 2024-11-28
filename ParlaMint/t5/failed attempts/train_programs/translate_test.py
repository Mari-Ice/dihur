import sys
#import comet_ml
from transformers import AutoTokenizer, Seq2SeqTrainingArguments, Seq2SeqTrainer
import evaluate
import torch
"""
experiment = comet_ml.Experiment(
    api_key="p9KsjgF50TWuwjBcXCQrS80j8",
    project_name="transformers_30",
    workspace="icecoldempress",
    auto_param_logging=True,
    auto_metric_logging=True,
    auto_histogram_weight_logging=True,
    auto_histogram_gradient_logging=True,
)

def prepare_dataset(text1, text2):
   dataset = [{"input_text": input_line.strip(), "target_text": reference_line.strip()} for input_line, reference_line in zip(text1, text2)]
   return dataset

import sentencepiece
import datasets
checkpoint = "google/mt5-small"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
print(tokenizer.encoding)
books = datasets.load_dataset("opus_books", "en-fr")

text1 = open(sys.argv[1], "r", encoding="utf-8").readlines()
text2 = open(sys.argv[2], "r", encoding="utf-8").readlines()
#dataset = prepare_dataset(text1, text2)
#print(dataset)

max_length = 256
print("tokenizing data")
def tokenize_data(dataset):
  inputs = ["translate: " + input["en"] for input in dataset["translation"]]
  targets = [target["fr"] for target in dataset["translation"]]
  model_inputs = tokenizer(inputs, text_target=targets, max_length=max_length, truncation=True, padding=True, return_tensors="pt")
  return model_inputs
def tokenize_custom_data(dataset):
   inputs = ["correct_text: " + input["input_text"] for input in dataset]
   targets = [target["target_text"] for target in dataset]
   model_inputs = tokenizer(inputs, text_target=targets, max_length=max_length, truncation=True, padding=True)
   
   return model_inputs

tokenized_dataset = tokenize_data(books["train"])

print("generating trainer")
from transformers import AutoModelForSeq2SeqLM
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

import numpy as np
def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]

    return preds, labels

metric = evaluate.load("cer")

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"bleu": result["score"]}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

from transformers import Seq2SeqTrainingArguments, DataCollatorForSeq2Seq

data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=checkpoint)
training_args = Seq2SeqTrainingArguments(
    output_dir="my_awesome_opus_books_model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=2,
    predict_with_generate=True,
)
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)
print("training")
trainer.train()