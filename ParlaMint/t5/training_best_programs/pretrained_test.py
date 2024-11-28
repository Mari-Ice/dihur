from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import sys

#input_text = open(sys.argv[1], "r", encoding="utf-8").read()

checkpoint = "./models/bigger_trainset_mistakes_01"
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

input_ids = tokenizer("correct Slovenian text: Politika je ze dolgo v malori dolgo smo teha spoznannja", return_tensors="pt").input_ids.to(model.device)

    # Generate output using the model
output_ids = model.generate(input_ids)

    # Decode the output tokens into text
output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print(output_text)