import sys
import os

ocrslo = open(sys.argv[1], 'r', encoding='utf-8').readlines()
origslo = open(sys.argv[2], 'r', encoding='utf-8').readlines()
ocrger = open(sys.argv[3], 'r', encoding='utf-8').readlines()
origger = open(sys.argv[4], 'r', encoding='utf-8').readlines()

ocr = []
orig = []

for i in range(min(len(ocrslo), len(ocrger))):
    # mix lines
    line_oc_s = ocrslo[i].strip()
    line_or_s = origslo[i].strip()
    line_oc_g = ocrger[i].strip()
    line_or_g = origger[i].strip()
    ocr.append(line_oc_s)
    ocr.append(line_oc_g)
    orig.append(line_or_s)
    orig.append(line_or_g)

i = 0
while((i+1) * 50000 < len(ocr)):
    open(f'./trainfiles/slo-ger/mixed_ocr_{i}.txt', 'w', encoding='utf-8').write("\n".join(ocr[i*50000:(i+1)*50000]))
    open(f'./trainfiles/slo-ger/mixed_orig_{i}.txt', 'w', encoding='utf-8').write("\n".join(orig[i*50000:(i+1)*50000]))
    i += 1

if(i*50000 < len(ocr)):
    open(f'./trainfiles/slo-ger/mixed_ocr_{i}.txt', 'w', encoding='utf-8').write("\n".join(ocr[i*50000:]))
    open(f'./trainfiles/slo-ger/mixed_orig_{i}.txt', 'w', encoding='utf-8').write("\n".join(orig[i*50000:]))
    


    