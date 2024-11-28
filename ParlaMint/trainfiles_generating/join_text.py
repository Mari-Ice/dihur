import sys
import os



text1 = open(sys.argv[1], "r", encoding="utf-8").read() ## 5 
text2 = open(sys.argv[2], "r", encoding="utf-8").read() ## 10
text5 = open(sys.argv[3], "r", encoding="utf-8").read() ## 5
text6 = open(sys.argv[4], "r", encoding="utf-8").read() ## 10
name = os.path.basename(sys.argv[1]).split("_")[0]

text = text1 + "\n" + text2
text_or = text5 + "\n" + text6

open(os.path.join(os.path.dirname(sys.argv[1]), f"{name}_ocr.txt"), "w", encoding="utf-8").write(text)
open(os.path.join(os.path.dirname(sys.argv[1]), f"{name}_orig.txt"), "w", encoding="utf-8").write(text_or)