from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
from thefuzz import fuzz
from difflib import SequenceMatcher
import os
from PIL import Image
import sys

api_key = sys.argv[2]
credentials = service_account.Credentials.from_service_account_file(api_key)

# Initialize the client
client = vision_v1.ImageAnnotatorClient(credentials=credentials)

image = sys.argv[1]

with open(image, "rb") as im:
    content = im.read()
p = Image.open(sys.argv[1])
p.show()
image = types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

txt_path = os.path.dirname(sys.argv[1])
name = os.path.splitext(os.path.basename(sys.argv[1]))[0].split("_modified")[0]
txt_path = os.path.join(txt_path, name + ".txt")

with open(txt_path, "r", encoding="utf-8") as txt:
    t = txt.read()
    tekst = "".join(t.split())


result = ""
if texts:
    re = texts[0].description
    result = "".join(re.split())
    matcher = SequenceMatcher(None, result, tekst)
    match = SequenceMatcher(None, re, t)
    r = fuzz.ratio(result, tekst)
    r2 = fuzz.ratio(re, t)
    if((r < 95) | (matcher.ratio() < 0.85)):
        print(re)
    print(str(r))
    print(str(r2))
    print(matcher.ratio())
    print(match.ratio())
    
else:
    print("no text detected")
