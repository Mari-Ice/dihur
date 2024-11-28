import sys
import os

from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import os
from PIL import Image
import sys


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

def fix_text_to_line(text):
    t = " ".join(text.split("\n"))
    return t


# preapre credentials and google client
print("berem credentials")
api_key = sys.argv[1]
credentials = service_account.Credentials.from_service_account_file(api_key)
print("intializing the client")
# Initialize the client
client = vision_v1.ImageAnnotatorClient(credentials=credentials)

dir = sys.argv[2]
print("preparing paths")
if(not(os.path.isdir(dir))):
    print("Please, provide the path to a directory.")
    exit(1)


ocr_file = ""
orig_file = ""

source_dir = sys.argv[2]

for dir in os.listdir(source_dir):
    dir = os.path.join(source_dir, dir)
    if(os.path.isdir(dir)):
        for i_name in os.listdir(dir):
            i_path = os.path.join(dir, i_name)
            if(i_path.endswith("_modified.jpg") | i_path.endswith("_modified.png")):
                print(i_path)
                # for each picture define its original page text and ocr text
                index = int(i_name.split("_page_modified")[0])
                original = open(os.path.join(dir, f"{index}_page.txt"), "r", encoding="utf-8").read()
                ocr = ocr_google(i_path, client)

                # get text in one line
                original = fix_text_to_line(original)
                ocr = fix_text_to_line(ocr)
                # append it to whole text
                orig_file += original + "\n"
                ocr_file += ocr + "\n"

name = os.path.basename(source_dir)

open(os.path.join(source_dir, f"{name}_original.txt"), "w", encoding="utf-8").write(orig_file)
open(os.path.join(source_dir, f"{name}_ocr.txt"), "w", encoding="utf-8").write(ocr_file)
