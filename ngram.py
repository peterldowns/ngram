sep = " " # separating symbol
keyjoin = lambda x: sep.join(map(str, x))
def calc_ngram(n, source):
	# calculates ngrams on lists. By default, tries to coerce everything
	# to a string and then sep.join the strings, but any suitable
	# joining function may be supplied.

	# n is the length of the gram. n=5 -> 5-gram. 
	source_len = len(source)
	print "Calculating n-gram level %d" % n
	grams = {}
	if source_len < n:
		return grams
	for i in xrange(source_len+1-n):
		gramkey = keyjoin(source[i:i+n]) # can't use lists as hashkeys.
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

def get_subgrams(ngram, grams):
	# keylist should be a sep separated string. If it's characters, have sep='\0'. If it's words, same thing works, but ' ' allows for pretty printing
	key = keyjoin(ngram)
	children = {}
	keylen = len(key)
	for gramkey in grams:
		if gramkey.count(sep) == (key.count(sep)+1): # only look at the next possible word
			if gramkey[0:keylen] == key and gramkey[keylen] == sep: # don't let annointment be chosen from an
				children[gramkey] = grams[gramkey]
	#DEBUGGING
	#print "key = %s" % key
	#print "children ="
	#for i in children:
		#print "\t%s" % i
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

from random import random
def rand_selection2(elements):
	#slow????
	totals = []
	running_total = 0
	for w in map(lambda x: x[1], elements):
		running_total += w
		totals.append(running_total)
	rnd = random()*running_total
	for i, total in enumerate(totals):
		if rnd < total:
			return elements[i][0]

def choose_child(existing, grams, level):
	# Given some existing amount of text to look at, look at most level elements
	# back and use that (and the count frequency dictionary, grams) to randomly
	# select the next element
	if level < 1:
		print "Level < 1; choosing a new word"
		return choice(list(set([i for i in grams if len(i.split(sep)) == 1]))) # choose a new word
	_slice = existing[-level:] # take at most the last level words
	pos_subgrams = get_subgrams(_slice, grams)
	
	#DEBUGGING
	#num_subgrams = len(pos_subgrams)
	#next_probs = {}
	#for key in pos_subgrams:
		#next_probs[" ".join(key.split(sep)[-1:])] = float(pos_subgrams[key])/num_subgrams
	#for a in next_probs:
		#print "P(%s | %s) = %f" % (a, _slice, next_probs[a])
	
	next_pop = [] # hold possible next words
	for gram in pos_subgrams:
		next_subgram = gram.split(sep)[-1] # for each whole child subgram, only look at the part that is different (the last element)
		count = pos_subgrams[gram]
		next_pop.append((next_subgram, count))

	if len(next_pop) == 0: # couldn't find anything; no valid next elements based on past history
		print "No children. Trying shallower level ( %d -> %d)" % (level, level-1)
		return choose_child(existing, grams, level-1) # ooh... recursive!
	else:	
		return rand_selection(next_pop)

def stochastic_walk(source, length, level, ngrams=None, sep='\0'):
	# Use a source to figure out probabilities of elements (characters, words, whatever)
	# appearing after other elements. Randomly choose a starting element from the source,
	# and then use those probabilities to randomly generate a new set of elements.
	if not ngrams:
		ngrams = calc_up_to_ngram(source, level)
	seed = choice(list(set(source)))
	print "Seed: %s" % seed
	out = [seed] # this is the output list
	
	while len(out) < length:
		_next = choose_child(out, ngrams, level)
		out.append(_next)
	return out

