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
# candidate_top_words_file = open("./test_code/candidates_top_ten_words.json") # this file is only word counts, not tfidf
candidate_top_words_file = open("./test_code/candidates_top_ten_words_tfidf.json")
candidate_top_ten_data = json.load(candidate_top_words_file)
candidate_response_file = open("./test_code/candidate_responses.json")
candidate_responses = json.load(candidate_response_file)
candidate_which_debates = open("./test_code/candidates_which_debates.json")
candidate_num_debates = json.load(candidate_which_debates)


def search_results(query, search_option):
    if search_option == 'candidate':
        # query is the key
        # pull the dictionary of words for that candidate
        try:
            top_ten_words = candidate_top_ten_data[query]

            # candidate responses
            responses = candidate_responses[query]

            return (top_ten_words, responses, {}) # {} is dummy dict
        except KeyError:
            return {}, {}, {}

    elif search_option == 'term':
        # get Total Mentions by Debate
        # debate date, location is key and term count is value
        total_mentions_debate = {}
        for key in debate_data_d:
            total_mentions_debate[key] = debate_data_d[key].get(query, 0)
        for key in debate_data_r:
            total_mentions_debate[key] = debate_data_r[key].get(query, 0)
        for key in debate_data_r_u: 
            total_mentions_debate[key] = debate_data_r_u[key].get(query, 0)

        # get Total Mentions by Candidate
        # candidate is key and term count is value
        total_mentions_candidate = {}
        for key in candidate_data:
            total_mentions_candidate[key] = candidate_data[key].get(query, 0)
        
        if any(total_mentions_debate.values()):
            # get Arguments and Interactions
            interactions = {}
            return (total_mentions_debate, total_mentions_candidate, candidate_num_debates) # interactions
        else:
            return {}, {}, {}
    
    return ({'nothing here':'hi'},{'nope':'nope'},{})
