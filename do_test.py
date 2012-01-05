# open don quixote and clean it up to be used as the source

print "Opening sourcefile (donquixote.txt)"
f = open("donquixote.txt", "rb")
dq = " ".join(f.readlines())
f.close()
import re
print "Cleaning sourcefile (donquixote.txt)"
dq = re.sub("[^a-zA-Z0-9_ ]", "", dq.strip().lower()) # lowercase all the characters.

# do the text generation. this takes a while.
from ngram import stochastic_walk, calc_up_to_ngram
n_grams = calc_up_to_ngram(dq, 5)
print "Walking (1-deep) ... "
a = stochastic_walk(dq, 50, 1, n_grams) 
print "\t%s" % a
print ""

print "Walking (3-deep) ... "
b = stochastic_walk(dq, 50, 3, n_grams)
print "\t%s" % b
print ""

print "Walking (5-deep) ... "
c = stochastic_walk(dq, 50, 5, n_grams)
print "\t%s" % c
print ""
