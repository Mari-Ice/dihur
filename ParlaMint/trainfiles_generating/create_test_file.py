import os
import sys
import subprocess
import random

# transforms each txt file into pdf --> adds wallpaper and converts to image 
# --> processes each image by given parameters --> saves the parameters in the main directory of output
# must give the path of programs with subprocesses as argument
def create_test(file, pr1, pr2, pr3, fonts, alignments, bgs, watermarks):
    # save the base name (for the name of the new directory)
    name = os.path.splitext(os.path.basename(file))[0]

    ## 1. fill template in word
    # we have to arrange the arguments for subprocedure:
    sectionsNum = random.randrange(1, 10) # num of sections
    command = ["python", pr1, file, name, str(sectionsNum)]
    for _ in range(sectionsNum):
        command.append(str(random.randrange(6))) # num of paragraphs
        font = random.choice(fonts)
        command.append(font) # font
        
        # for german fonts allow only bigger fonts
        if("AuldMagick" in fonts):
             command.append(str(random.randrange(14, 18))) # font size
        else:
            command.append(str(random.randrange(11, 14))) # font size
        command.append(random.choice(alignments)) # alignment
        command.append(str(random.choice([0, 1]))) # 0= one column, 1= two columns
        command.append(str(random.randrange(30))) # bold %
        command.append(str(random.randrange(10))) # underlined %
        command.append(str(random.randrange(20))) # italic %
        command.append(str(random.randrange(30))) # colored %
    
    output = subprocess.check_output(command)
    print(output)
    
    # at this point a pdf named name.pdf exists
    ## 2. add background to the pdf and convert in images
    # path to pdf
    path = os.path.join(os.path.dirname(file), name)
    
    command1 = ["python", pr2, os.path.join(path, name + ".pdf", ), name + "_modified.pdf", random.choice(bgs), str(random.uniform(0.8, 1.15))]
    output = subprocess.check_output(command1)
   
    print(output)
    ## 3. process all the images
    images = []

    # add images paths to the list
    for filename in os.listdir(path):
        f_path = os.path.join(path, filename)
        if(os.path.isfile(f_path)):
            if(f_path.endswith(".png") | f_path.endswith(".jpg")):
                images.append(f_path)
    # save the parameters in a text file
    path_commands = os.path.join(path, "commands.txt")
    with open(path_commands, "w", encoding="utf-8") as commands:
        commands.write(" ".join(command) + "\n\n")
        commands.write(" ".join(command1) + "\n\n")
        
        for image in images:
            command2 = ["python", pr3, image]
            command2.append(str(random.choice([0, 1, 3]))) # erosion kernel 0, 1, 3
            command2.append(str(random.choice([0, 1]))) # dilation kernel
            command2.append(str(random.choice([1, random.randrange(3)]))) # downscale 3
            command2.append(str(random.uniform(0.7, 1.5))) # brighten
            command2.append(str(random.uniform(0.7, 1.4))) # contrast
            command2.append(str(random.uniform(0.7, 15))) # sharpen
            rotate = random.randrange(4) - random.randrange(4) # rotate for degree in [-3, 3]
            command2.append(str(rotate)) # rotate
            # we don't allow rotate with curving of side
            if(rotate != 0):
                command2.append(str(0)) #side=0
            else:
                command2.append(str(random.choice([0, 1, 2]))) # side [0, 1, 2]
            command2.append(str(random.randrange(95, 105))) # c1
            command2.append(str(random.randrange(195, 205))) # c2
            command2.append(str(random.uniform(0.001, 0.1))) # c3 - amplitude
            command2.append(str(random.randrange(10))) # salt-pepper % 
            command2.append(random.choice(watermarks)) # watermark link
            command2.append(str(random.choice([0, 1, 3]))) # flip [0, 1, 3] - the orientation of watermark image
            command2.append(str(random.choice([0, random.uniform(0.1, 0.8)]))) # colorize
            command2.append(str(random.choice([0, 1, 3, 5]))) # blur kernel
            output = subprocess.check_output(command2)

            print(output)
            commands.write(" ".join(command2) + "\n\n")
        
    
    return True


#######################################################################################################
##############################################    MAIN    #############################################
#######################################################################################################

## argv: txt_directory, backgrounds_directory, watermarks_directory, 
# fill_layout path, add_background path, image_processing path, german/slovene text
fill_layout = sys.argv[4]
add_background = sys.argv[5]
image_processing = sys.argv[6]
german = sys.argv[7]
path = sys.argv[1]
if(not(os.path.isdir(path))):
    print("Please, provide the path to a directory.")
    exit(1)
print("preparing files")
files = []
for file_name in os.listdir(path):
    file_path = os.path.join(path, file_name)
    if(os.path.isfile(file_path)):
        if(file_path.endswith(".txt")):
            files.append(file_path)
            print(file_path)

# fonts 
latin_fonts = ["Cambria","Times New Roman", "Helvetica", "Candara", "News Gothic MT", "Bahnschrift Light", "Cambria Math", "HoloLens MDL2 Assets", "Mongolian Baiti", "Sitka Banner"]
gothic_fonts = ["Old English Text MT", "Minster No 3", "Olde English Regular", "AuldMagick", "DS Luthersche", "Kleist-Fraktur", "The Quality Brave"]
alignments = ["left", "distribute"]
print("preparing backgrounds")
bgs = []
bgs_path = sys.argv[2]
if(os.path.isdir(bgs_path)):
    for file_name in os.listdir(bgs_path):
        file_path = os.path.join(bgs_path, file_name)
        if(os.path.isfile(file_path)):
            if(file_path.endswith(".jpg") | file_path.endswith(".png")):
                bgs.append(file_path)
else:
    bgs.append(bgs_path)
print("preparing watermarks")
watermarks = []
wat_path = sys.argv[3]
if(os.path.isdir(wat_path)):
    for file_name in os.listdir(wat_path):
        file_path = os.path.join(wat_path, file_name)
        if(os.path.isfile(file_path)):
            if(file_path.endswith(".jpg") | file_path.endswith(".png")):
                watermarks.append(file_path)
else:
    watermarks.append(wat_path)
fonts = []
if(german == "1"):
    fonts = gothic_fonts
else:
    fonts = latin_fonts
for file in files:
    print("working on file")
    create_test(file, fill_layout, add_background, image_processing, fonts, alignments, bgs, watermarks)
    
    