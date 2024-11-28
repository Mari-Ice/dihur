import sys
import os

file = open(sys.argv[1], "r", encoding="utf-8").read()

new_file = file.replace("[[", "(").replace("]]", ")").replace("[", "(").replace("]", ")")

file_cleaned = open(os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1]).split(".txt")[0] + "_cleaned.txt"), "w", encoding="utf-8")
file_cleaned.write(new_file)