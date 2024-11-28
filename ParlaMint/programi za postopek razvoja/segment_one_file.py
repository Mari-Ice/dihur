from trankit import Pipeline
import sys
import os

if(len(sys.argv) < 2):
    print("Please provide the target directory for sentence segmentation.")
    exit(1)

path = sys.argv[1]
if(not os.path.isfile(path)):
    print("This is not an appropriate file")
    exit(1)
if(not path.endswith(".txt")):
    print("Not a txt file")
    
    
pipeline = Pipeline("slovenian")
#pipeline.add("german")
#pipeline.add("serbian")
#pipeline.set_auto(True)


f = (open(path, "r", encoding="utf-8")).read()
    #print(f)
if(f != ""):
    sentences = pipeline.ssplit(f)
    sentences = sentences["sentences"]
    sentences = [sentence["text"] for sentence in sentences]
        #print(sentences)
    processed_text = '\n'.join(sentences)
    print(processed_text.split()[0])
    name = os.path.basename(path).split(".txt")[0] + "_segmented.txt"
    dir = os.path.dirname(path)
    new_file = os.path.join(dir, name)
    out = open(new_file, "w", encoding="utf-8")
    out.write(processed_text)
   
