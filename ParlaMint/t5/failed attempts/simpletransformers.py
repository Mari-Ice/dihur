import pandas as pd
from tqdm import tqdm
import json
import difflib
from sklearn.model_selection import train_test_split
import sys
import os
import torch

os.environ['TRANSFORMERS_CACHE'] = '/mnt/ten/marijaabsec/simpletransformers/train/cache'
print(os.getenv("TRANSFORMERS_CACHE"))


ocr = open(sys.argv[1], "r", encoding="utf-8").readlines()
orig = open(sys.argv[2], "r", encoding="utf-8").readlines()
ocr = [line.strip() for line in ocr]
orig = [line.strip() for line in orig]

data = {"prefix": "correct Slovenian text:", "ocr": ocr, "orig": orig}
train_data = pd.DataFrame(data)

train_data.rename(columns={"ocr": "input_text", "orig": "target_text"}, inplace=True)
train, test = train_test_split(train_data, test_size=0.1)

print(train.head())

from simpletransformers.t5 import T5Model, T5Args


model_args = T5Args()
model_args.num_train_epochs = 5
model_args.max_length = 512
model_args.save_model_every_epoch = False
model_args.fp16 = False
model_args.overwrite_output_dir = True
model_args.train_batch_size = 1
model_args.eval_batch_size = 1

model = T5Model(
    "mt5",
    "google/mt5-base",
    cache_dir="./cache",
    args=model_args,
    cuda_device=1
)
model.train_model(train)
