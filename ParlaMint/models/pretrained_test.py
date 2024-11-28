from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import sys

input_text = open(sys.argv[1], "r", encoding="utf-8").readlines()

checkpoint = "./mistakes_01"
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)


def decode_input(text):
    input_ids = tokenizer("correct Slovenian text: " + text, return_tensors="pt").input_ids.to(model.device)

    # Generate output using the model	
    output_ids = model.generate(input_ids)

    # Decode the output tokens into text
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text

with open("result.txt", "w", encoding="utf-8") as f:
    for line in input_text:
        f.write(decode_input(line.strip()) + "\n")

