import os
import sys
import difflib

file = open(sys.argv[1], "r", encoding="utf-8").read()

file = file.replace("— ", "").replace("- ", "").replace("(", "").replace(")", "").replace("\n", " ")


open("result_better.txt", "w", encoding="utf-8").write(file)
corrected_ocr = open(sys.argv[2], "r", encoding="utf-8").read()

corrected_ocr = corrected_ocr.replace("\n", " ")
open("ocr_new.txt", "w", encoding="utf-8").write(corrected_ocr)
matcher = difflib.SequenceMatcher(None, file, corrected_ocr)
ratio = matcher.ratio()

print(ratio)