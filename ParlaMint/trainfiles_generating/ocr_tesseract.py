from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import os
from PIL import Image
import sys
import subprocess
import pytesseract as tsr


def ocr_tesseract(image, language):
    return tsr.image_to_string(image, lang=language)

tsr.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
print("Listing the files")
input = sys.argv[1]
files = []
if(os.path.isdir(input)):
    for elt in os.listdir(input):
        elt = os.path.join(input, elt)
        if(os.path.isdir(elt)):
            for file in os.listdir(elt):
                file = os.path.join(elt, file)
                if(os.path.isfile(file)):
                    
                    if(file.endswith("_modified.png") | file.endswith("_modified.jpg")):
                        files.append(file)
                        print(file)

print("Performing ocr - saving as ocr_[pagenum].txt")
for file in files:
    number = os.path.basename(file).split("_page")[0]
    with open(os.path.join(os.path.dirname(file), "ocr_tesseract_" + number + ".txt"), "w", encoding="utf-8") as ocrFile:
        ocrFile.write(ocr_tesseract(file, sys.argv[2]))