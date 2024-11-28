import sys
import os

file = open(sys.argv[1], "r", encoding="utf-8").read().split()
text = ""
for f in file:
    if(("ParlaMint" in f) | ("Parla" in f)):
        text += "\n"
    text += f + " "

open("corrected_ocr.txt", "w", encoding="utf-8").write(text)
