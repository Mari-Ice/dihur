import sys

file1 = open(sys.argv[1], "r", encoding="utf-8").readlines()
file2 = open(sys.argv[2], "r", encoding="utf-8").readlines()

i = 50000
j = 1
while(i < len(file1)):
    newf1 = open(sys.argv[1] + "_" + str(j) + ".txt", "w", encoding="utf-8").write("".join(file1[i - 50000:i]))
    newf2 = open(sys.argv[2] + "_" + str(j) + ".txt", "w", encoding="utf-8").write("".join(file2[i - 50000:i]))
    j += 1
    i += 50000

if(i - 50000 < len(file1)):
    open(sys.argv[1] + "_" + str(j) + ".txt", "w", encoding="utf-8").write("".join(file1[i - 50000:]))
    open(sys.argv[2] + "_" + str(j) + ".txt", "w", encoding="utf-8").write("".join(file2[i - 50000:]))

