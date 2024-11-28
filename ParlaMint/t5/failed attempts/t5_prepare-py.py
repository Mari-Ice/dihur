import pandas as pd
from jiwer import wer, cer
import json
import difflib
from tqdm import tqdm
import os
import comet_ml
import sys

os.environ['TRANSFORMERS_CACHE'] = '/mnt/ten/marijaabsec/t5train/cache'
print(os.getenv("TRANSFORMERS_CACHE"))

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from simpletransformers.t5 import T5Model, T5Args
import torch
import Levenshtein
from sklearn.metrics import make_scorer


if torch.cuda.is_available():
    device = torch.device("cuda")
    print("GPU is available.")
else:
    device = torch.device("cpu")
    print("Using CPU.")

experiment = comet_ml.Experiment(
    api_key="p9KsjgF50TWuwjBcXCQrS80j8",
    project_name="simple_transformers_30",
    workspace="icecoldempress",
    auto_param_logging=True,
    auto_metric_logging=True,
    auto_histogram_weight_logging=True,
    auto_histogram_gradient_logging=True,
)
def calculate_cer(references, predictions):
    cer_scores = []
    for pred, ref in zip(predictions, references):
        cer = Levenshtein.distance(ref, pred) / max(len(ref), len(pred))
        cer_scores.append(cer)
    experiment.log_metric("cer", cer_scores)
    return cer_scores

# Create a CER scorer in sklearn format
cer_scorer = make_scorer(
    score_func=calculate_cer,
    greater_is_better=False,  # Lower CER is better
    needs_proba=False,
    needs_threshold=False
)

## prepare the training model
model_args = T5Args()
model_args.num_train_epochs = 5
model_args.max_length = 256
model_args.save_model_every_epoch = False
model_args.fp16 = False
model_args.overwrite_output_dir = True
model_args.train_batch_size = 1
model_args.eval_batch_size = 1
model_args.evaluate_during_training = True

model = T5Model(
    "mt5",
    "google/mt5-base",
    args=model_args,
    cuda_device=1
)
print("initialised mt5")

## prepare training files
ocr_text = open(sys.argv[1], "r", encoding="utf-8").readlines()
orig_tekst = open(sys.argv[2], "r", encoding="utf-8").readlines()
data = {"prefix": "fix the errors in the text:", "ocr text": ocr_text, "orig text": orig_tekst}
train_data = pd.DataFrame(data)

train_data.rename(columns={"ocr text": "input_text", "orig text": "target_text"}, inplace=True)
train, test = train_test_split(train_data, test_size=0.1)

train = train[["input_text", "target_text"]]
train["prefix"] = "fix the errors in the text:"

print("data prepared, proceed to training")
## finetune the model: 




model.train_model(train, eval_data=test, accuracy=accuracy_score)
print("training complete")
model.save_model("./models")
print("model saved")


print("--------------------------------\ntesting with test data")
### prediction of test data
"""
test['original_text_for_t5'] = 'fix the errors in the text: ' + test['original_text']
test.head()
test_predicted = model.predict(test.original_text_for_t5.tolist())
for tekst in test_predicted:
    print(tekst)
"""
