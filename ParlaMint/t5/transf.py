import comet_ml
import os
import torch
torch.cuda.set_device(0)

import transformers
import sys
experiment = comet_ml.Experiment(
    api_key="p9KsjgF50TWuwjBcXCQrS80j8",
    project_name="simple_transformers_30",
    workspace="icecoldempress",
    auto_param_logging=True,
    auto_metric_logging=True,
    auto_histogram_weight_logging=True,
    auto_histogram_gradient_logging=True,
)

#print(transformers.__version__)

checkpoint = "google/mt5-base"

from datasets import load_dataset, load_metric, Dataset

ocr = [line.strip() for line in open(sys.argv[1], "r", encoding="utf-8").readlines()][:500]
orig = [line.strip() for line in open(sys.argv[2], "r", encoding="utf-8").readlines()][:500]
l = len(ocr)
train_percent = l // 10

dataset = Dataset.from_dict({"input_text": ocr[train_percent:], "target_text": orig[train_percent:]})



from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
prefix = "correct Slovenian text: "
max_length = 256

def preprocess_function(examples):
    
    try:
        
        inputs = [prefix + ex for ex in examples["input_text"]]
        targets = [ex for ex in examples["target_text"]]
        model_inputs = tokenizer(inputs, max_length=max_length, truncation=True)

        with tokenizer.as_target_tokenizer():
            labels = tokenizer(targets, max_length=max_length, truncation=True)
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    except Exception as e:
        print("Error in preprocess_function:", e)
        print("Examples:", examples)
        raise e


tokenized_input = dataset.map(preprocess_function, batched=True)
print(tokenized_input)
eval = Dataset.from_dict({"input_text": ocr[:train_percent], "target_text": orig[:train_percent]})



eval_tokenized_input = eval.map(preprocess_function, batched=True)

from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer

model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

args = Seq2SeqTrainingArguments(
    "transformer",
    evaluation_strategy = "epoch",
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    save_total_limit=3,
    num_train_epochs=5,
    predict_with_generate=True,
)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

import numpy as np


import evaluate
metric = evaluate.load("cer")

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
   
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [label.strip() for label in decoded_labels]

    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"cer": result}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

trainer = Seq2SeqTrainer(
    model,
    args,
    train_dataset=tokenized_input,
    eval_dataset=eval_tokenized_input,
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,

)
print("training the model!!!")
torch.cuda.set_device(0)
print(torch.cuda.current_device())
trainer.train()

trainer.save_model("./models")