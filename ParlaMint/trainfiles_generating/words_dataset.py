import os
import sys
import random
import string

def createMistake(word):
    if(len(word) <= 1):
        return word
    indx = random.randrange(len(word) - 1)
    if(indx % 2 == 0): 
        return word
    mistake = random.randrange(3)
    replace_char = random.choice(string.ascii_letters + string.digits)
    newWord = ''
    if(mistake == 0):
       newWord = word[:indx] + word[indx+1:]
    elif(mistake == 1):
        newWord = word[:indx] + replace_char + word[indx:] 
    else:
        newWord = word[:indx] + word[indx+1:]

    return newWord

##corrects divided words and removes newlines, replaces [][] with ()()
file1 = open(sys.argv[1], "r", encoding="utf-8").read().replace("-\n", " ").replace("\n", " ").replace("[[", "(").replace("]]", ")").replace("[", "(").replace("]", ")")
words1 = file1.split()[:50000]

i = 0

f1 = open("orig_words_train.txt", "w", encoding="utf-8")
f2 = open("ocr_words_train.txt", "w", encoding="utf-8")
while(i < len(words1)):
    
    if(i == 0):
        f1.write(words1[i])
        f2.write(createMistake(words1[i].strip()))
    else:
        f1.write("\n" + words1[i])
        f2.write("\n" + createMistake(words1[i].strip()))
    
    i += 1

    
