from trankit import Pipeline
import sys
import os

if(len(sys.argv) < 2):
    print("Please provide the target directory for sentence segmentation.")
    exit(1)

path = sys.argv[1]
dir_path = os.path.dirname(path)
files = []
## stores all chosen files from the directory to list files
if(not (os.path.isdir(path))):
    print("Input is one file")
    name = os.path.basename(path)
    if(not(name.endswith(".txt"))):
        print("Not a .txt file or directory. FAILURE")
        exit(1)
    files.append(path)
    dir_path = path
else:
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if(os.path.isfile(file_path)):
            if(file_path.endswith(".txt")):
                files.append(file_path)
                print(file_path)
    dir_name = os.path.basename(path) + "_ssegmented"
    dir_path = os.path.join(dir_path, dir_name)
    os.mkdir(dir_path)
    
    
pipeline = Pipeline("slovenian")
#pipeline.add("german")
#pipeline.add("serbian")
#pipeline.set_auto(True)

processed_files = []
for file in files:
    f = (open(file, "r", encoding="utf-8")).read()
    #print(f)
    if(f != ""):
        sentences = pipeline.ssplit(f)
        sentences = sentences["sentences"]
        sentences = [sentence["text"] for sentence in sentences]
        #print(sentences)
        processed_text = '\n'.join(sentences)
        #print(processed_text)
        processed_files.append(processed_text)
        
new_path = os.path.join(dir_path, "segmented.txt")
with open(new_path, "w", encoding="utf-8") as new_file:
    for i in range(len(processed_files)):
        new_file.write(processed_files[i])
        if(i < len(processed_files)):
            new_file.write("\n")


