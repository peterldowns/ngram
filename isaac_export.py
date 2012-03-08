# open don quixote and clean it up to be used as the source
print "Opening sourcefile (donquixote.txt)"
f = open("donquixote.txt", "rb")
dq = " ".join(f.readlines())
f.close()

# clean up the source string
import re
print "Cleaning sourcefile (donquixote.txt)"
dq = re.sub("[^a-zA-Z0-9_ ]", "", dq.strip().lower()) # lowercase all the characters.

dq.split(" ") # dq as a string is a list of characters. make it a list of words.

# calculate the n_grams at a given level and store it to a dict
from ngram import stochastic_walk, calc_up_to_ngram
n_grams = calc_up_to_ngram(dq, 1) # 1 is the level, basically word counts

# save the ngram dictionary to a file using pickle
import pickle
with open("donquixote_ngram_dict.pk", "w") as of:
	pickle.dump(n_grams, of)

for i in n_grams:
	print i, n_grams[i]
# to load the ngram dictionary:
# with open("donquixote_ngram_dict.pk", "r") as if:
#	n_grams = pickle.load(if)

