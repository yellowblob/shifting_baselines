#compares the vocabulary of two txt files

import sys

# load ascii text
filename1 = sys.argv[1]
filename2 = sys.argv[2]
raw_text1 = open(filename1).read()
raw_text2 = open(filename2).read()

raw_text = raw_text1 + raw_text2

# get all chars from texts
chars = sorted(list(set(raw_text)))

f= open("vocabulary.txt","w+")
f.write(''.join(chars))
f.close()

n_vocab = len(chars)
print("Total Vocab: ", n_vocab)
print(chars)