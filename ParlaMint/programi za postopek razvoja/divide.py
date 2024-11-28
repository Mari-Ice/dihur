import sys
import os

## take input text file and split text by spaces
# file = array of words in a file
file = open(sys.argv[1], "r", encoding="utf-8").read().split()

for i in range(3, 70):
    # generate text with i words in one line 
    text = ""
    length = len(file)
    j = 0
    while(j + i - 1 < length):
        # give i words in each line and a "\n" at the end of each line
        for k in range(i):
            text += file[j + k] + " "
        text += "\n"
        # move j for i positions ahead
        j = j + i
    # if we haven't used all of the words, we use the last few as well
    while(j < length):
        text += file[j]
        j = j + 1
    # we write into a temp txt file
    open(f'{i}_temp.txt', "w", encoding="utf-8").write(text)

    i = i + 3

