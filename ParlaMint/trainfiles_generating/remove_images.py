import sys
import os

dir = sys.argv[1]

for file_name in os.listdir(dir):
    file_path = os.path.join(dir, file_name)
    if(os.path.isdir(file_path)):
        for i_name in os.listdir(file_path):
            i_path = os.path.join(file_path, i_name)
            if(i_path.endswith(".jpg") | i_path.endswith(".png")):
                os.remove(i_path)