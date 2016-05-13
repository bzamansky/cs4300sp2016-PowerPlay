# get searched candidate
# get that candidate's text (debates and statements), put it in one thing
# get everyone else's text (debates and statements)
# fighting words

import json
from fighting_words import bayes_compare_language

cand_words = {} # value is string of everything key says

with open('candidates_top_words.json', 'r') as f:
	words = json.load(f)
	for cand,dictionary in words.iteritems():
		everything = ""
		for word,count in dictionary.iteritems():
			if count != 0:
				everything += (word+" ")*count
		cand_words[cand] = everything

# with open('candidate_statements.json', 'r') as f:
# 	statements = json.load(f)
# 	for cand,words in statements.iteritems():
# 		print words
# 		# for w in words:
# 		# 	if w not in [',', '.', '!', '?', '-']:
# 		# 		cand_words[cand] += w + " "

print cand_words['jindal']

# all_results = {}
# for cand,words in cand_words.iteritems():
# 	all_other_words = ""
# 	for c,w in cand_words.iteritems():
# 		if c != cand:
# 			all_other_words += w

# 	results = bayes_compare_language([words], [all_other_words]) # results is list of (word, score)
# 	top = results[:10]
# 	bottom = results[-10:]
# 	all_results[cand] = top + bottom


# # put results in json file
# with open('fighting_words.json', 'w') as f:
# 	json.dump(all_results, f)