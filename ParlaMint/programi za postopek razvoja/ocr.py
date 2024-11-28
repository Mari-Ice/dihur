from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import os
from PIL import Image
import sys
import subprocess

def ocr_google(image, client):
    
    with open(image, "rb") as im:
        content = im.read()
    p = Image.open(image)
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description

print("berem credentials")
api_key = sys.argv[1]
credentials = service_account.Credentials.from_service_account_file(api_key)
print("intializing the client")
# Initialize the client
client = vision_v1.ImageAnnotatorClient(credentials=credentials)

print("Listing the files")
input = sys.argv[2]
files = []
if(os.path.isdir(input)):
    for file in os.listdir(input):
        file = os.path.join(input, file)
        if(os.path.isfile(file)):
            if(file.endswith("_modified.png") | file.endswith("_modified.jpg")):
                files.append(file)
                print(file)

print("Performing ocr - saving as ocr_[pagenum].txt")
for file in files:
    number = os.path.basename(file).split("_page")[0]
    with open(os.path.join(input, "ocr_" + number + ".txt"), "w", encoding="utf-8") as ocrFile:
        ocrFile.write(ocr_google(file, client))