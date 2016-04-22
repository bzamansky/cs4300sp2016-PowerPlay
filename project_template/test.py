from .models import Docs
import os
import Levenshtein
import json
from collections import defaultdict


def read_file(n):
	path = Docs.objects.get(id = n).address;
	file = open(path)
	transcripts = json.load(file)
	return transcripts

def _edit(query, msg):
    return Levenshtein.distance(query.lower(), msg.lower())

def find_similar(q):
	transcripts = read_file(1)
	result = []
	for transcript in transcripts:
		for item in transcript:
			m = item['text']
			result.append(((_edit(q, m)), m))

	return sorted(result, key=lambda tup: tup[0])

# JACKIE'S NEW CODE
# query is a... query
# option is either 'term' or 'candidate', from the radio button selection
def find_similar_advanced(query, option):
	if option == 'term':
		transcripts = read_file(1) # read the TERM json file
	elif option == 'candidate':
		transcripts = read_file(1) # read the CANDIDATE json file
	for transcript in transcripts:
		for item in transcript:
			m = item['text']
			result.append(((_edit(q, m)), m))

	return sorted(result, key=lambda tup: tup[0])

# PUT THIS IN PREPROCESSING SO DON'T NEED TO DO IT EVERY TIME
# debate data, so available throughout this script
# NOTE: debate word data is in 3 files (dem, rep, rep undercard) because one file too bit for GitHub :(
debate_data_file_dem = open("./test_code/debates_top_words_d.json") # democratic debates
debate_data_file_rep = open("./test_code/debates_top_words_r.json") # republican debates
debate_data_file_rep_under = open("./test_code/debates_top_words_r_u.json") # republican undercard debates
debate_data_d = json.load(debate_data_file_dem)
debate_data_r = json.load(debate_data_file_rep)
debate_data_r_u = json.load(debate_data_file_rep_under)
candidate_data_file = open("./test_code/candidates_top_words.json")
candidate_data = json.load(candidate_data_file)

# option_1 is T/F for candidate, option_2 is T/F for term
def search_results(query, option_1, option_2):
	# if option is candidate
	if option_1 == True:
		pass
	# if option is term
	if option_2 == True:
		# get Total Mentions by Debate
		# debate is key and term count is value
		total_mentions_debate = defaultdict()
		for key in debate_data_d.keys():
			total_mentions_debate[key] += debate_data_d[key][query]
		for key in debate_data_r.keys():
			total_mentions_debate[key] += debate_data_r[key][query]
		for key in debate_data_r_u.keys(): 
			total_mentions_debate[key] += debate_data_r_u[key][query]

		# get Total Mentions by Candidate
		# candidate is key and term count is value
		total_mentions_candidate = {}
		for key in candidate_data.keys():
			total_mentions_candidate[key] = candidate_data[key][query]
		
		# get Arguments and Interactions
		interactions = {}
		return (total_mentions_debate, total_mentions_candidate, interactions)
	
	return ({'nothing here':'hi'},{'nope':'nope'},{})
	






	