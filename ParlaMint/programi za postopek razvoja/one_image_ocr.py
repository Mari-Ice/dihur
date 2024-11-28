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

input = sys.argv[2]

with open((input + "_ocr.txt"), "w", encoding="utf-8") as ocrFile:
    ocrFile.write(ocr_google(input, client))