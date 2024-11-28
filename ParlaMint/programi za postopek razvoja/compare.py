
import sys
from thefuzz import fuzz
import difflib

# sys.argv: original_text_path other_text_path


orig = sys.argv[1]
sec = sys.argv[2]

orig = open(orig, "r", encoding="utf-8").read()
sec = open(sec, "r", encoding="utf-8").read()

orig1 = "".join(orig.split())
sec1 = "".join(sec.split())

matcher = difflib.SequenceMatcher(None, sec, orig)
matcher1 = difflib.SequenceMatcher(None, sec1, orig1)

match = fuzz.ratio(sec, orig)
match1 = fuzz.ratio(sec1, orig1)

print("original ocr result:")
print("difflib:")
print(matcher.ratio())
print(matcher1.ratio())
print("thefuzz:")
print(match)
print(match1)

if(len(sys.argv) == 4):
    norm = sys.argv[3]
    norm = open(norm, "r", encoding="utf-8").read()
    norm1 = "".join(norm.split())
    matcher_ = difflib.SequenceMatcher(None, norm, orig)
    matcher_1 = difflib.SequenceMatcher(None, norm1, orig1)
    match_ = fuzz.ratio(norm, orig)
    match_1 = fuzz.ratio(norm1, orig1)
    print("normalised text result:")
    print("difflib:")
    print(matcher_.ratio())
    print(matcher_1.ratio())
    print("thefuzz:")
    print(match_)
    print(match_1)



