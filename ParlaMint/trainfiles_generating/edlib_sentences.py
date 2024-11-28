import edlib
import sys

orig = open(sys.argv[1], "r", encoding="utf-8").readlines()
ocr = open(sys.argv[2], "r", encoding="utf-8").readlines()


ends = [".", "!", "?"]

for k in range(len(orig)):
    use_orig = orig[k]
    use_ocr = ocr[k]
    print("-----------------------------------------------------------")
    orig_lines = []
    i = 0
    for j in range(len(use_orig)):
        if (use_orig[j] in ends):
            orig_lines.append(use_orig[i:j+1])
            i = j + 1

