from .models import Docs
import os
import Levenshtein
import json


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
debate_data_file = open("./test_code/debates_top_words.json") # this data is organized by date (so debate)
debate_data = json.load(debate_data_file)
candidate_data_file = open("./test_code/candidates_top_words.json")
candidate_data = json.load(candidate_data_file)

# # TODO: GET ALL WORDS BY DEBATE, store as debate --> all words in that debate
# all_words_debate = {} # dictionary with date as key and words spoken as value
# for debate in debate_data:
# 	debate_words = ""
# 	for line in debate['tran']:
# 		debate_words = debate_words + line['speech']
# 	all_words_debate[debate['date']] = debate_words

# option_1 is T/F for candidate, option_2 is T/F for term
def search_results(query, option_1, option_2):
	# if option is candidate
	if option_1 == True:
		pass
	# if option is term
	if option_2 == True:
		# get Total Mentions by Debate
		# debate is key and term count is value
		total_mentions_debate = {}
		for key in debate_data.keys():
			total_mentions_debate[key] = debate_data[key][query]
		# get Total Mentions by Candidate
		# candidate is key and term count is value
		total_mentions_candidate = {}
		for key in candidate_data.keys():
			total_mentions_candidate[key] = candidate_data[key][query]
		# get Arguments and Interactions
		interactions = {}
		return (total_mentions_debate, total_mentions_candidate, interactions)
	return ({'nothing here':'hi'},{'nope':'nope'},{})
	






	