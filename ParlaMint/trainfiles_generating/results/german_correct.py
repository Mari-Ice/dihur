import os
import sys
import os
from PIL import Image
import sys
import random
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import difflib

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
    input_ids = tokenizer("correct text: " + text, return_tensors="pt").input_ids.to(model.device)

    # Generate output using the model	
    output_ids = model.generate(input_ids)

    # Decode the output tokens into text
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text

checkpoint = "oliverguhr/spelling-correction-german-base"
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

dir = sys.argv[1]

files = []
for f in os.listdir(dir):
    if(f.endswith("_page.txt")):
        files.append(f) ## you get only the txt files

resultG = 0
resultGg90 = 0
resultT = 0
resultTg90 = 0
ocr_diff_G = 0
ocr_diff_T = 0
ocr_diff_G90 = 0
ocr_diff_T90 = 0
numG = 0
numT = 0

files = random.sample(files, (len(files) // 10) + 1)
##you take 10% of files for the sample
for file in files:
    file_path = os.path.join(dir, file)
    print(file)
    pageNum = file.split("_page")[0]
    originalText = open(file_path, "r", encoding="utf-8").read().replace("[", "").replace("]", "").replace("\n", " ")
    ocrGoogle = open(os.path.join(dir, f"ocr_{pageNum}.txt")).read().replace("\n", " ").replace("[", "").replace("]", "")
    ocrTesseract = open(os.path.join(dir, f"ocr_tesseract_{pageNum}.txt")).read().replace("\n", " ").replace("[", "").replace("]", "")

    ## break ocrText into lines of 7 words and connect it into a whole text
    ocr = transform(ocrGoogle.split())
    correctedText1 = [correctOcr(o) for o in ocr]
    correctedText1 = " ".join(correctedText1)
    ocr_t = transform(ocrTesseract.split())
    correctedText2 = [correctOcr(o) for o in ocr_t]
    correctedText2 = " ".join(correctedText2)

    orig_g = max((difflib.SequenceMatcher(None, originalText, ocrGoogle).ratio()), (difflib.SequenceMatcher(None,ocrGoogle, originalText).ratio()))
    orig_corrG = max((difflib.SequenceMatcher(None, originalText, correctedText1).ratio()), (difflib.SequenceMatcher(None, correctedText1, originalText).ratio()))
    orig_t = max((difflib.SequenceMatcher(None, originalText, ocrTesseract).ratio()), (difflib.SequenceMatcher(None, ocrTesseract, originalText).ratio()))
    orig_corrT = max((difflib.SequenceMatcher(None, originalText, correctedText2).ratio()),(difflib.SequenceMatcher(None, correctedText2, originalText).ratio()))
    #print("diff: original-ocrG text --" +  str(orig_g))
    #print("diff: original-correctedOcrG text --" + str(orig_corrG))
    #print("diff: original-ocrT text -- " +  str(orig_t))
    #print("diff: original-correctedOcrT text --" +  str(orig_corrT))
    #open("resultG.txt", "w", encoding="utf-8").write(correctedText1)
    #open("resultT.txt", "w", encoding="utf-8").write(correctedText2)
    #print()
    ocr_diff_G += orig_g
    ocr_diff_T += orig_t
    resultG += orig_corrG
    resultT += orig_corrT
    if(orig_g >= 0.9):
        numG += 1
        resultGg90 += orig_corrG
        ocr_diff_G90 += orig_g
    if(orig_t >= 0.9):
        numT += 1
        resultTg90 += orig_corrT
        ocr_diff_T90 += orig_t

ocr_diff_G /= len(files)
ocr_diff_T /= len(files)
resultG /= len(files)
resultT /= len(files)
if(numG > 0):
    resultGg90 /= numG
    ocr_diff_G90 /= numG
if(numT > 0):
    ocr_diff_T90 /= numT
    resultTg90 /= numT
with open(os.path.join(dir, "evaluation.txt"), "w", encoding="utf-8") as f:
    f.write(f"Google ocr vs corrected: {ocr_diff_G} : {resultG}")
    if(numG > 0):
        f.write(f"Google for ocr >= 0.9 similarity: {ocr_diff_G90} : {resultGg90}")
    f.write(f"Tesseract ocr vs corrected: {ocr_diff_T} : {resultT}")
    if(numT > 0):
        f.write(f"Tesseract for ocr >= 0.9 similarity: {ocr_diff_T90} : {resultTg90}")