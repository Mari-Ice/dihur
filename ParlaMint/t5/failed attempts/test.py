from simpletransformers.t5 import T5Model, T5Args
from transformers import T5Tokenizer
import sys
model = T5Model("mt5", "/mnt/ten/marijaabsec/t5train/mt5_train/outputs/mt5_base_7_8_2023")
tokenizer = T5Tokenizer.from_pretrained("google/mt5-base")

test_data = []
with open(sys.argv[1], "r", encoding="utf-8") as file:
    for line in file:
        test_data.append(line.strip())

print(str(len(test_data)))
for t in test_data:
    print(t)

inputs = tokenizer.batch_encode_plus(["fix the errors in the text: " + data for data in test_data], padding=True, return_tensors="pt")
outputs = model.model.generate(inputs["input_ids"], max_length=2048, num_beams=4, early_stopping=True)
predictions = tokenizer.batch_decode(outputs, skip_special_tokens=True)

print(str(len(predictions)))
for p in predictions:
    print(p)