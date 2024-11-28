import edlib
import sys
import os

def count_alphabeth(line):
    alphabeth = []
    for l in line:
        if(not (l in alphabeth)):
            alphabeth.append(l)
    return alphabeth, len(alphabeth)
def interpret_cigar(cigar, substr_len):
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    
    eq = 0
    insert = 0
    delete = 0
    mismatch = 0

    cur_num = ""
   
    first_eq = 0
    first_eq_bool = True
    last_eq = 0
    cur_index = 0
    for a in cigar: 
        ## if the substring is whole found
        if((eq >= substr_len) | (last_eq - first_eq >= 5 * substr_len)):
            break
        if (a in nums):
            cur_num += a
        else:
            cur_num = int(cur_num)
            
            
            if(a == "I"):
                insert += cur_num
            else:
                
                if(a == "="):
                    if(first_eq_bool):
                        first_eq = cur_index
                        last_eq = cur_index + cur_num
                        first_eq_bool = False
                    else:
                        last_eq = cur_index + cur_num
                    eq += cur_num
                else:
                    
                    if(a == "X"):
                        mismatch += cur_num
                    elif(a == "D"):
                        delete += cur_num
                cur_index += cur_num
            cur_num = ""
            
    return {"=": eq, "I": insert, "D": delete, "X": mismatch, "start": first_eq, "end": last_eq}

def align_texts(orig_lines, use_ocr):
    res_orig = []
    res_ocr = []
    j = 0 ## index for tracking all proccessed text to this point
    delted_lines = 0
    for line in orig_lines:
        l = len(line)
        use_ocr1 = use_ocr[j:j+3*l]
        
        #print("line:     " + line)
        #print(use_ocr1)
        ##                input  target  
        al = edlib.align(line, use_ocr1, task="path") 
        
        cigar = al.get("cigar")
        nums = interpret_cigar(cigar, l) if cigar != None else None
        #print(cigar)
        #print(nums)
        
        if((nums != None) ):
            #print("rate: " + str((nums.get("=") / l)))  
            #print("ocr:      " + use_ocr1[nums.get("start"):nums.get("end")])
            if((nums.get("=") / l) >= 0.8):
                
                res_orig.append(line)
                res_ocr.append(use_ocr1[nums.get("start"):nums.get("end")])
                j += nums.get("end")
            else:
                delted_lines += 1
    return res_orig, res_ocr, delted_lines

def align_text_for_n_words(orig, ocr, orig_path, ocr_path, n):
    res_orig = []
    res_ocr = []
    all_lines = 0
    all_deleted = 0

    for k in range(len(orig)):
        
        use_orig = orig[k]
        use_ocr = ocr[k]
        orig_lines = []
        i = 0
        space = 0
        for j in range(len(use_orig)):
            if(use_orig[j] == " "):
                space += 1
            if(space == n):
                orig_lines.append(use_orig[i:j+1])
                i = j+1
                space = 0
        #print("total lines: " + str(len(orig_lines)))
        all_lines += len(orig_lines)
        
        ## 2. Začnemo z iskanjem z alignmentom? Nek treshold določimo za dopuščanje različnosti? Se je smiselno pomikati naprej? nočemo preveč brisati vsega (sedaj ostalo 10%, hočemo 90%)
        ## premikamo se naprej po ocr, če kje večji preskok še vedno iščemo od tam naprej, sicer to kasneje pobrišemo

        align_orig, align_ocr, deleted_lines = align_texts(orig_lines, use_ocr)
        res_orig += align_orig
        res_ocr += align_ocr
        all_deleted += deleted_lines

    print(f"{n}-words: all lines: " + str(all_lines))
    print(f"{n}-words: all deleted lines: " + str(all_deleted) + " that is " + str(all_deleted / all_lines * 100) + "%")
    if((all_deleted / all_lines * 100) >= 15):
        print("Please check imput data manually for misaligned lines (pages) or unwanted empty pages.")

    orig_name = os.path.join(orig_path, os.path.basename(sys.argv[1]).split(".txt")[0] + f"_training_orig_{n}.txt")
    ocr_name = os.path.join(ocr_path, os.path.basename(sys.argv[2]).split(".txt")[0] + f"_training_ocr_{n}.txt")
    open(orig_name, "w", encoding="utf-8").write("\n".join(res_orig))
    open(ocr_name, "w", encoding="utf-8").write("\n".join(res_ocr))


###################################################################################################################
###################################################################################################################
## MAIN:

orig = open(sys.argv[1], "r", encoding="utf-8").readlines()
ocr = open(sys.argv[2], "r", encoding="utf-8").readlines()

orig_path = os.path.dirname(sys.argv[1])
ocr_path = os.path.dirname(sys.argv[2])
## input files should be one line per page of training set (ocr images etc) -- created by create_tain_files.py

## 1. določimo mesta koncev povedi v originalu (na roke), list indeksov je rezultat, glede na to razdelimo original na "vrstice" array teh odsekov
res_orig = []
res_ocr = []
all_lines = 0
all_deleted = 0

for k in range(len(orig)): ## align se dela paroma po straneh (k-ta vrstica je k-ta stran)
    
    use_orig = orig[k]
    use_ocr = ocr[k]
    ends = [".", "!", "?"]
    orig_lines = []
    i = 0
    for j in range(len(use_orig)):
        if(use_orig[j] in ends):
            orig_lines.append(use_orig[i:j+1])
            i = j+1
    #print("total lines: " + str(len(orig_lines)))
    all_lines += len(orig_lines)
    
    ## 2. Začnemo z iskanjem z alignmentom? Nek treshold določimo za dopuščanje različnosti? Se je smiselno pomikati naprej? nočemo preveč brisati vsega (sedaj ostalo 10%, hočemo 90%)
    ## premikamo se naprej po ocr, če kje večji preskok še vedno iščemo od tam naprej, sicer to kasneje pobrišemo

    align_orig, align_ocr, deleted_lines = align_texts(orig_lines, use_ocr)
    res_orig += align_orig
    res_ocr += align_ocr
    all_deleted += deleted_lines

print("all lines: " + str(all_lines))
print("all deleted lines: " + str(all_deleted) + " that is " + str(all_deleted / all_lines * 100) + "%")
if((all_deleted / all_lines * 100) >= 15):
    print("Please check imput data manually for misaligned lines (pages) or unwanted empty pages.")

orig_name = os.path.join(orig_path, os.path.basename(sys.argv[1]).split(".txt")[0] + "_training_orig.txt")
ocr_name = os.path.join(ocr_path, os.path.basename(sys.argv[2]).split(".txt")[0] + "_training_ocr.txt")
open(orig_name, "w", encoding="utf-8").write("\n".join(res_orig))
open(ocr_name, "w", encoding="utf-8").write("\n".join(res_ocr))


##################################################################################################################################
##################################################################################################################################

## 3. glede na dobljen par vrstic po povedih: generiramo večbesedne vrstice, ki niso vezane na povedi! -- nikjer več kot 256 znakov!

## po 5 besed
align_text_for_n_words(orig, ocr, orig_path, ocr_path, 5)
## po 10 besed
align_text_for_n_words(orig, ocr, orig_path, ocr_path, 10)
## po 15 besed
#align_text_for_n_words(orig, ocr, orig_path, ocr_path, 15)
## po 20 besed
#align_text_for_n_words(orig, ocr, orig_path, ocr_path, 20)