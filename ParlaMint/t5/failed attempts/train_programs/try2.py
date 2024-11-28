import comet_ml
import sys

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
import evaluate
import numpy as np
from sklearn.model_selection import train_test_split

comet_ml.init(project_name="my-first-try", api_key="p9KsjgF50TWuwjBcXCQrS80j8")

checkpoint = "google/mt5-small"
tokenizer = AutoTokenizer.from_pretrained(checkpoint, use_fast=False)

def prepare_dataset(input_file, reference_file):
    with open(input_file, "r", encoding="utf-8") as f:
        input_lines = f.readlines()

    with open(reference_file, "r", encoding="utf-8") as f:
        reference_lines = f.readlines()

    dataset = [{"input_text": input_line.strip(), "target_text": reference_line.strip()} for input_line, reference_line in zip(input_lines, reference_lines)]
    return dataset


## popravi
def preprocess_function(examples):
    inputs = ["correct Slovenian text: " + example["input_text"] for example in examples]
    targets = [example["target_text"] for example in examples]
    model_inputs = tokenizer(inputs, text_target=targets, max_length=256, truncation=True, padding=True, return_tensors="pt")
    return model_inputs



model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

dataset = prepare_dataset(sys.argv[1], sys.argv[2])
print(dataset[0])
#train, test = train_test_split(dataset, test_size=0.1)
#print(train[0])
#print(test[0])
tokenized_train = preprocess_function(dataset)
#tokenized_test = preprocess_function(test)
print(tokenized_train)


data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=checkpoint)

metric = evaluate.load("cer")

def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]

    return preds, labels

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"cer": result["score"]}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

"""
training_args = Seq2SeqTrainingArguments(
    output_dir="./output_dir",      # Change to your preferred output directory
    per_device_train_batch_size=4,   # Adjust batch size as needed
    save_total_limit=2,
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    eval_steps=100,
    logging_dir="./logs",            # Change to your preferred logging directory
    logging_steps=10,
    save_steps=500,
    num_train_epochs=5,              # Adjust number of epochs
    report_to="comet_ml",
    predict_with_generate=True,    
    data_collator=data_collator
    
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train,
)

def compute_cer(predictions, labels):
    cer_sum = 0
    total_chars = 0
    for pred, label in zip(predictions, labels):
        cer_sum += lev.distance(pred, label)
        total_chars += len(label)
    cer = cer_sum / total_chars
    return cer
def compute_metrics(p):
    predictions = [tokenizer.decode(pred, skip_special_tokens=True) for pred in p.predictions]
    labels = [example["target_text"] for example in p.label_ids]
    
    cer = compute_cer(predictions, labels)
    loss = p.loss.mean().item()

    return {"cer": cer, "loss": loss}

trainer.compute_metrics = compute_metrics

trainer.train()
"""