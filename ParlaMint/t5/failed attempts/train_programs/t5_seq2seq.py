import pandas as pd
from jiwer import wer, cer
import numpy as np
import json
import difflib
from tqdm import tqdm
import os
import comet_ml
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoConfig, AutoModel, TrainingArguments, Trainer
import torch
import evaluate



def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max-length", truncation=True)

def preprocess_function(dataset, tokenizer):
    inputs = [data for data in dataset["input_text"].tolist()]
    targets = dataset["target_text"].tolist()
    model_inputs = tokenizer(inputs, text_target=targets, max_length=256, truncation=True, padding=True)
    return model_inputs

def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]

    return preds, labels


def compute_metrics(eval_preds):
    metric = evaluate.load("cer")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

os.environ['TRANSFORMERS_CACHE'] = '/mnt/ten/marijaabsec/t5train/cache'
os.environ['COMET_API_KEY'] = 'p9KsjgF50TWuwjBcXCQrS80j8'
TOKENIZERS_PARALLELISM = False
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("GPU is available.")
else:
    device = torch.device("cpu")
    print("Using CPU.")

experiment = comet_ml.get_global_experiment()

comet_ml.init(project_name="testing-with-comet-transformers-t5")
os.environ["COMET_LOG_ASSETS"] = "True"

#experiment.log_metric("cer", 1.0)
model_name = "google/mt5-small"
config = AutoConfig.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

## prepare training files
# 
#prefix = "correct_Slovenian_text: "

ocr_text = open("./2000_ocr_cleaned_training_ocr.txt", "r", encoding="utf-8").readlines()
orig_tekst = open("./2000_original_cleaned_training_orig.txt", "r", encoding="utf-8").readlines()

data = {"ocr text": ocr_text, "orig text": orig_tekst}
train_data = pd.DataFrame(data)
train_data.rename(columns={"ocr text": "input_text", "orig text": "target_text"}, inplace=True)


train, test = train_test_split(train_data, test_size=0.1)
train = preprocess_function(train, tokenizer)
test = preprocess_function(test, tokenizer)


##metric = evaluate.load("bleu")-------------------------------------METRICS!
print("data prepared, proceed to training")



train_args = TrainingArguments(
    output_dir="./models",
    overwrite_output_dir=True,
    evaluation_strategy="steps", 
    eval_steps=100, 
    save_steps=500,
    num_train_epochs=5,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    logging_dir="./runs",
    logging_steps=100,
    learning_rate=1e-4,
    save_strategy="steps",
    load_best_model_at_end=True,
    metric_for_best_model="myMetric",
    fp16=False,
)

## prepare the training model

model = AutoModel.from_pretrained(model_name)

#####
trainer = Trainer(
    model=model,
    args=train_args,
    train_dataset=train,
    eval_dataset=test,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)
print("initialised mt5")


## finetune the model: 
trainer.train()


print("training complete")
model.save_model("./models/")
print("model saved")
experiment.log_model("MT5_train_testing_comet", model, overwrite=True)
experiment.end()


print("--------------------------------\ntesting with test data")
