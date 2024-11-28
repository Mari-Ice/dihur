import sys
import os

dir = sys.argv[1]
text = ""
for file in os.listdir(dir):
    file = os.path.join(dir, file)
    if(os.path.isfile(file)):
        if(file.endswith(".txt")):
            print(file + " is txt file")
            text += open(file, "r", encoding="utf-8").read()

dir_bname = os.path.basename(dir)

with open(os.path.join(dir, dir_bname + "_all.txt"), "w", encoding="utf-8") as f:
    f.write(text)