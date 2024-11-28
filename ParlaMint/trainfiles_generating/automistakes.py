import os
import sys
import random
import string

"""
addes mistakes to text given in argv
"""

ocr = open(sys.argv[1], "r", encoding="utf-8").readlines()

for i in range(len(ocr)):
    line_ocr = ocr[i]
    ## randomly make 5% of mistakes
    indxNum = (len(line_ocr) - 1) * 5 // 100
    for j in range(indxNum): ## change 2 with indxNum
        indx = random.randrange(len(line_ocr) - 1)
        # zbrisi
        # dodaj
        # zamenjaj
        replace_char = random.choice(string.ascii_letters + string.digits)

        mistake = random.randrange(3)
        if(mistake == 0):
            ocr[i] = line_ocr[:indx] + line_ocr[indx+1:]
        elif(mistake == 1):
            ocr[i] = line_ocr[:indx] + replace_char + line_ocr[indx:]
        else:
            ocr[i] = line_ocr[:indx] + replace_char + line_ocr[indx+1:]

open(os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+"_mistakes.txt"), "w", encoding="utf-8").write("".join(ocr))
