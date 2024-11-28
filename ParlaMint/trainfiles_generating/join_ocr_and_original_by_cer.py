import sys
import os

import os
import sys
import difflib

def fix_text_to_line(text):
    t = " ".join(text.split("\n")).replace("[[", "(").replace("]]", ")").replace("[", "").replace("]", "")
    return t


if(not(os.path.isdir(sys.argv[1]))):
    print("Please, provide the path to a directory.")
    exit(1)


ocr_file = ""
orig_file = ""

num_deleted_files = 0
num_all = 0

source_dir = sys.argv[1]

for dir in os.listdir(source_dir):
    dir = os.path.join(source_dir, dir)
    if(os.path.isdir(dir)):
        for i_name in os.listdir(dir):
            i_path = os.path.join(dir, i_name)
            if(i_path.endswith("_page.txt")):
                print(i_path)
                num_all += 1
                ## for each page text define its ocr text and difference
                index = int(i_name.split("_page.txt")[0])
                original = open(i_path, "r", encoding="utf-8").read()
                ocr = open(os.path.join(dir,"ocr_" + str(index) + ".txt"), "r", encoding="utf-8").read()

                ## let text in one line
                original = fix_text_to_line(original)
                ocr = fix_text_to_line(ocr)
                matcher = difflib.SequenceMatcher(None, ocr, original)
                matcher1 = difflib.SequenceMatcher(None, original, ocr)
                ratio = matcher.ratio()
                ratio1 = matcher1.ratio()
                if(max(ratio, ratio1) >= 0.85 and max(ratio, ratio1) <= 0.99):
                    ## append it to whole text
                    orig_file += original + "\n"
                    ocr_file += ocr + "\n"
                else:
                    num_deleted_files += 1

name = os.path.basename(source_dir)

open(os.path.join(source_dir, f"{name}_original.txt"), "w", encoding="utf-8").write(orig_file)
open(os.path.join(source_dir, f"{name}_ocr.txt"), "w", encoding="utf-8").write(ocr_file)
print("all: " + str(num_all))
print("deleted: " + str(num_deleted_files))
