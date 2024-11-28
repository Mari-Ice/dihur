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
    if(len(texts) == 0):
        return ""
    return texts[0].description

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


#prepares paths to all images in order
dirs = []
images = []
for file_name in os.listdir(dir):
    file_path = os.path.join(dir, file_name)
    if(os.path.isdir(file_path)):
        dirs.append(file_path)
        imgs = []
        for i_name in os.listdir(file_path):
            i_path = os.path.join(file_path, i_name)
            if(i_path.endswith("_modified.jpg") | i_path.endswith("_modified.png")):
                imgs.append(i_path)
        
        imgs.sort(key=lambda path: int(os.path.basename(path).split("_page")[0]))
        for im in imgs:
            images.append(im)

result = ""

for image in images: 
    ocr_result = " ".join(ocr_google(image, client).split())
    print(image)
    open(os.path.join(os.path.dirname(image), "ocr_" + os.path.basename(image).split("_page")[0] + ".txt"), "w", encoding="utf-8").write(ocr_result)
    result += "\n" + ocr_result
new_dir = os.path.join(dir, "ocr_result")
os.mkdir(new_dir)
with open(os.path.join(new_dir, "result.txt"), "w", encoding="utf-8") as txt:
    txt.write(result)

##print(subprocess.check_output(["python", "./sentence_segmentation.py", new_dir]))