import os
import sys 

file = open(sys.argv[1], "r", encoding="utf-8").read()
file = file.replace("-\n", "")

file = file.replace("\n", " ")


f = open(sys.argv[1] + "_corrected.txt", "w", encoding=	"utf-8")

if(len(file.split()) <= 7):
    f.write(file)
else:
    words = file.split()
    i = 7 
    while (i < len(words)):
        f.write(" ".join(words[i - 7:i]) + "\n")
        i += 7
    if(i - 7 < len(words)):
        f.write(" ".join(words[i-7:]))


