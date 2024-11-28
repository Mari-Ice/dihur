import comet_ml
import os
import pandas
import numpy
comet_ml.init(project_name="my-first-try", api_key="p9KsjgF50TWuwjBcXCQrS80j8")

PRE_TRAINED_MODEL_NAME = "google/mt5-small"
SEED = 42

from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2Se2TrainingArguments, Seq2SeqTrainer, EarlyStoppingCallback
from datasets import load_dataset

raw_datasets = load_dataset("imdb")
tokenizer = MT5Tokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)


tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)

from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

train_dataset = tokenized_datasets["train"].shuffle(seed=SEED).select(range(200))
eval_dataset = tokenized_datasets["test"].shuffle(seed=SEED).select(range(200))

from transformers import AutoModel

model = AutoModel.from_pretrained(
    PRE_TRAINED_MODEL_NAME, num_labels=2
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def get_example(index):
    return eval_dataset[index]["text"]


def compute_metrics(pred):
    experiment = comet_ml.get_global_experiment()

    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="macro"
    )
    acc = accuracy_score(labels, preds)

    if experiment:
        epoch = int(experiment.curr_epoch) if experiment.curr_epoch is not None else 0
        experiment.set_epoch(epoch)
        experiment.log_confusion_matrix(
            y_true=labels,
            y_predicted=preds,
            file_name=f"confusion-matrix-epoch-{epoch}.json",
            labels=["negative", "postive"],
            index_to_example_function=get_example,
        )

    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}

os.environ['COMET_MODE']='ONLINE'
os.environ['COMET_LOG_ASSETS']='TRUE'

training_args = TrainingArguments(
    seed=SEED,
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=1,
    do_train=True,
    do_eval=True,
    evaluation_strategy="steps",
    eval_steps=25,
    save_strategy="steps",
    save_total_limit=10,
    save_steps=25,
    per_device_train_batch_size=8,
    report_to=["comet_ml"],
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
    data_collator=data_collator,
)
trainer.train()