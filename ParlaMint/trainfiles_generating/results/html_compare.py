import os
import sys
import os
import sys
import difflib

def transform(text):
    newText = []
    i = 7
    while(i < len(text)):
        newText.append(" ".join(text[i - 7:i]))
        i += 7
    if(i - 7 < len(text)):
        newText.append(" ".join(text[i-7:]))
    return newText

dir = sys.argv[1]

files = []
for f in os.listdir(dir):
    if(f.endswith("_page.txt")):
        files.append(f) ## you get only the txt files



for file in files:
    file_path = os.path.join(dir, file)
    print(file)
    pageNum = file.split("_page")[0]
    
    ocrGoogle = open(os.path.join(dir, f"ocr_{pageNum}.txt"), 'r', encoding='utf-8').read().replace("\n", " ").replace("[", "").replace("]", "").replace("—", "")
    corrected = open(os.path.join(dir, f"{pageNum}_page.txt.corrected.txt"), 'r', encoding='utf-8').read().replace("—", "")
    orig = open(os.path.join(dir, f"{pageNum}_page.txt"), 'r', encoding='utf-8').read().replace("\n", " ").replace("[", "").replace("]", "").replace("—", "")
    ## break ocrText into lines of 7 words and connect it into a whole text
    ocr = (ocrGoogle.split(','))
    corr = (corrected.split(','))
    orig = (orig.split(','))
    d = difflib.HtmlDiff(wrapcolumn=100)
    diff_html = d.make_file(fromlines=ocr, tolines=corr, fromdesc='ocr', todesc='corrected')
    diff_orig = d.make_file(fromlines=orig, tolines=corr, fromdesc='Original', todesc='Corrected')
    with open(os.path.join(dir, f"{pageNum}.html"), 'w', encoding="utf-8") as f:
        f.write(diff_html)
        f.write(str(max((difflib.SequenceMatcher(None, " ".join(orig), " ".join(ocr)).ratio()), (difflib.SequenceMatcher(None," ".join(ocr), " ".join(orig)).ratio()))))
        f.write('\n')
        f.write(diff_orig)
        f.write(str(max((difflib.SequenceMatcher(None, " ".join(orig), " ".join(corr)).ratio()), (difflib.SequenceMatcher(None," ".join(corr), " ".join(orig)).ratio()))))
        f.write('\n')
        f.write(str(max((difflib.SequenceMatcher(None, " ".join(orig), " ".join(ocr)).ratio()), (difflib.SequenceMatcher(None," ".join(ocr), " ".join(orig)).ratio()))))
