#splits the files into training and validation data

import sys
import math

# load ascii text
filename = sys.argv[1]
raw_text = open(filename).read()
#raw_text = raw_text.lower()

# reduce vocabulary

n_chars = len(raw_text)
splitat = math.ceil(n_chars*0.9)

print(n_chars)
print(splitat)

train_text, val_text = raw_text[:splitat], raw_text[splitat:]

filename = filename[:filename.find("_")]

f= open(filename + "_train.txt","w+")
f.write(train_text)
f.close()

f= open(filename + "_val.txt","w+")
f.write(val_text)
f.close()