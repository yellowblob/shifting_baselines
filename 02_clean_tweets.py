#reduces vocabulary of tweets to get faster learning

import sys

# load ascii text from file handed over as command line argument
filename = sys.argv[1]
raw_text = open(filename).read()
#raw_text = raw_text.lower()

# reduce vocabulary by replacing special characters with more common ones
unwanted_chars = [
					["à","a"],
					["á","a"],
					["â","a"],
					["ầ","a"],
					["ć","c"],
					["è","e"],
					["é","e"],
					["í","i"],
					["ï","i"],
					["ı","i"],
					["ñ","n"],
					["ñ","n"],
					["ó","o"],
					["ô","o"],
					["ö","o"],
					["ộ","o"],
					["ğ","g"],
					["ú","u"],
					["ĺ","l"],
					["ö","o"],
					["ō","o"],
					["ễ","e"],
					["ž","z"],
					["ｒ","r"],
					["t","t"],
					["ｔ","t"],			
					["–","-"],
					["—","-"],
					["―","-"],
					["‘","'"],
					["’","'"],
					["\"","'"],
					["“","'"],
					["”","'"],
					["„","'"],
					["…","..."],
					["`","'"],
					["´","'"],
					["′","'"],
					["‼","!!"],
					["\x92","'"],
					["\xa0","'"],
					["\u200a"," "],
					["\u200b"," "],
					["\u200e",""],
					["\u200f",""],
					["●","•"],
					["☀","*"],
					["\U0010fc00",""],
					["《","«"],
					["➡","➜"],
					["❤","♥"],
					['️',""],
					["🇦","[A]"],
					['🇧',"[B]"],
					["🇨","[C]"],
					["🇪","[E]"],
					["🇫","[F]"],
					["🇬","[G]"],
					["🇮","[I]"],
					["🇯","[J]"],
					["🇰","[K]"],
					["🇱","[L]"],
					["🇲","[M]"],
					["🇳","[N]"],
					["🇴","[O]"],
					["🇵","[P]"],
					["🇷","[R]"],
					["🇸","[S]"],
					["🇹","[T]"],
					["🇺","[U]"],
					["🇽","[X]"],
					["\ufeff",""],
					["√","✓"],
					["✔","✓"],
					["⬆","↑"],
					["⬇","↓"],
					["&amp;","&"],

]

for i in range(len(unwanted_chars)):
	raw_text = raw_text.replace(unwanted_chars[i][0],unwanted_chars[i][1])

#cut off file extension from filename
filename = filename[:filename.find("_")]

#write cleaned text to file
f= open(filename + "_cleaned.txt","w+")
f.write(raw_text)
f.close()

# check the number of chars and display some statistics
chars = sorted(list(set(raw_text)))

n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)
print(chars)