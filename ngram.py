sep = "\0" # separating symbol

def calc_ngram(n, source, keyjoin=lambda x: sep.join(map(str, x)) ):
	# calculates ngrams on lists. By default, tries to coerce everything
	# to a string and then sep.join the strings, but any suitable
	# joining function may be supplied.
	source_len = len(source)
	print "Calculating n-gram level %d" % n
	grams = {}
	if source_len < n:
		return grams
	for i in xrange(source_len+1-n):
		gramkey = keyjoin(source[i:i+n])
		grams.setdefault(gramkey, 0)
		grams[gramkey] += 1
	return grams

def calc_up_to_ngram(source, level=1):
	# Calculates 1 through n-grams on a given source and combines them
	# into one big dictionary
	print "Creating ngram-count dictionary ... "
	counts = {}
	for n in xrange(1, level+2): # +2: need 1 to offset xrange, 1 to look ahead for possibilities
		counts.update(calc_ngram(n, source))
	return counts

def get_subgrams(keystr, grams):
	# key should be a sep separated string
	#keystr = sep.join(map(str, keylist)) #uncomment this to work with non-characters
	children = {}
	for gramkey in grams:
		if gramkey.count(sep) == (keystr.count(sep)+1): # only look at the next possible word
			if gramkey[0:len(keystr)] == keystr:
				children[gramkey] = grams[gramkey]
	#DEBUGGING
	#print "key = %s" % key
	#print "children ="
	#for i in children:
	#	print "\t%s" % i
	return children

from random import choice
def rand_selection(elements):
	# elements is a (value, count) tuple
	# given those (value, count) tuples, randomly pick a value
	# (but bias by count). Higher count = greater probability
	# note: there *must* be a better way to do this instead of
	#	filling a list (slow!)
	population = []
	for val, count in elements:
		for i in xrange(count):
			population.append(val)
	return choice(population)

def choose_child(existing, grams, level):
	# Given some existing amount of text to look at, look at most level elements
	# back and use that (and the count frequency dictionary, grams) to randomly
	# select the next element
	if level < 1:
		print "Level = 0; choosing a new word"
		return choice(list(set([i for i in grams if len(i.split()) == 1]))) # choose a new word
	slice = sep.join(existing.split(sep)[-level:]) # take at most the last level words
	pos_subgrams = get_subgrams(slice, grams)
	num_subgrams = len(pos_subgrams)
	
	#DEBUGGING
	#next_probs = {}
	#for key in pos_subgrams:
	#	next_probs[" ".join(key.split()[-1:])] = float(pos_subgrams[key])/num_subgrams
	#for a in next_probs:
	#	print "P(%s | %s) = %f" % (a, slice, next_probs[a])
	
	next_pop = [] # hold possible next words
	for el in pos_subgrams:
		key = el.split(sep)[-1] # for each whole child subgram, only look at the part that is different (the last element)
		count = pos_subgrams[el]
		next_pop.append((key, count))

	if len(next_pop) == 0: # couldn't find anything; no valid next elements based on past history
		print "\"%s\" has no children. Trying shallower level ( %d -> %d)" % (slice,level, level-1)
		return choose_child(existing, grams, level-1) # ooh... recursive!
	else:	
		return rand_selection(next_pop)

def stochastic_walk(source, length, level, ngrams=None):
	# Use a source to figure out probabilities of elements (characters, words, whatever)
	# appearing after other elements. Randomly choose a starting element from the source,
	# and then use those probabilities to randomly generate a new set of elements.
	if not ngrams:
		ngrams = calc_up_to_ngram(source, level)
	seed = choice(list(set(source)))
	print "Seed: %s" % seed
	text = [seed]
	
	while len(text) < length:
		next = choose_child(sep.join(text), ngrams, level)
		text.append(next)
	return "".join(text)

