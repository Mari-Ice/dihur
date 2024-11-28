import os
import sys
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import os
from PIL import Image
import sys
import random
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import difflib



def ocr_google(image, client):
    
    with open(image, "rb") as im:
        content = im.read()
    p = Image.open(image)
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if(len(texts) == 0):
        return ""
    return texts[0].description

def transform(text):
    newText = []
    i = 7
    while(i < len(text)):
        newText.append(" ".join(text[i - 7:i]))
        i += 7
    if(i - 7 < len(text)):
        newText.append(" ".join(text[i-7:]))
    return newText

def correctOcr(text):
    input_ids = tokenizer("correct Slovenian text: " + text, return_tensors="pt").input_ids.to(model.device)

    # Generate output using the model	
    output_ids = model.generate(input_ids)

    # Decode the output tokens into text
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text


print("berem credentials")
api_key = sys.argv[1]
credentials = service_account.Credentials.from_service_account_file(api_key)
print("intializing the client")
# Initialize the client
client = vision_v1.ImageAnnotatorClient(credentials=credentials)

source_dir = sys.argv[2]
checkpoint = sys.argv[3]
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
num = 0
result_ocr = 0
result_corrected = 0
num_bad_exceptions = 0

for dir in os.listdir(source_dir):
    dir = os.path.join(source_dir, dir)
    if(os.path.isdir(dir)):
        for i_name in os.listdir(dir):
            i_path = os.path.join(dir, i_name)
            if(i_path.endswith("_modified.jpg") | i_path.endswith("_modified.png")):
                print(i_path)
                ## for each picture define its original page text and ocr text
                index = int(i_name.split("_page_modified")[0])
                original = open(os.path.join(dir, f"{index}_page.txt"), "r", encoding="utf-8").read().replace("\n", " ").replace("[", "").replace("]", "")
                ocr = ocr_google(i_path, client).replace("\n", " ").replace("[", "").replace("]", "")
                
                
                ocr_evalutation = max(difflib.SequenceMatcher(None, original, ocr).ratio(), difflib.SequenceMatcher(None, ocr, original).ratio())
                if(ocr_evalutation < 0.9):
                    num_bad_exceptions += 1
                else:
                    result_ocr += ocr_evalutation
                    corrected_ocr = " ".join([correctOcr(o) for o in transform(ocr.split())])
                    result_corrected += max(difflib.SequenceMatcher(None, original, corrected_ocr).ratio(), difflib.SequenceMatcher(None, corrected_ocr, original).ratio())
                    num += 1


print(f"FINISHED WITH EVALUATION: \n RESULTS: \nocr similarity: {result_ocr / num}\nautocorrect similarity: {result_corrected / num}")
print("bad exceptions: " + str(num_bad_exceptions))
open("evaluation.txt", "w", encoding="utf-8").write(f"FINISHED WITH EVALUATION: \n RESULTS: \nocr similarity: {result_ocr / num}\nautocorrect similarity: {result_corrected / num}\nBAD EXCEPTIONS: {num_bad_exceptions}")

            


