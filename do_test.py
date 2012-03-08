# open don quixote and clean it up to be used as the source
print "Opening sourcefile (prideandprejudice.txt)"
f = open("prideandprejudice.txt", "rb")
dq = " ".join(f.readlines())
f.close()
import re
print "Cleaning sourcefile (prideandprejudice.txt)"
dq = re.sub("[^a-zA-Z0-9_ ]", "", dq.strip().lower()) # lowercase all the characters.

sep = '\0'

# uncomment the next two lines to analyze words
sep = ' '
dq = dq.split(sep)

# do the text generation. this takes a while.
from ngram import stochastic_walk, calc_up_to_ngram
n_grams = calc_up_to_ngram(dq, 5)

print "Walking (1-deep) ... "
a = stochastic_walk(dq, 50, 1, n_grams, sep) 
print "\t%s" % sep.join(a)
print ""

print "Walking (3-deep) ... "
b = stochastic_walk(dq, 50, 3, n_grams, sep)
print "\t%s" % sep.join(b)
print ""

print "Walking (5-deep) ... "
c = stochastic_walk(dq, 50, 5, n_grams, sep)
print "\t%s" % sep.join(c)
print ""
