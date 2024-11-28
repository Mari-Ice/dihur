import os
import sys
import os
from PIL import Image
import sys
import random

dir = sys.argv[1]

files = []
for f in os.listdir(dir):
    if(f.endswith("_page.txt")):
        files.append(f) ## you get only the txt files

##you take 10% of files for the sample
for file in files:
    file_path = os.path.join(dir, file)
    print(file)
    pageNum = file.split("_page")[0]
    originalText = open(file_path, "r", encoding="utf-8").read().replace("[", "").replace("]", "").replace("\n", " ")
    ocrGoogle = open(os.path.join(dir, f"ocr_{pageNum}.txt")).read().replace("\n", " ").replace("[", "").replace("]", "")
    name = file.split('.')[0]
    with open(os.path.join(dir, f"{name}_for_comparation.txt"), "w", encoding="utf-8") as f:
        f.write(ocrGoogle)