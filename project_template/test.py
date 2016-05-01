from .models import Docs
import os
# import Levenshtein
import json
#from collections import defaultdict

def read_file(n):
	path = Docs.objects.get(id = n).address;
	file = open(path)
	transcripts = json.load(file)
	return transcripts

# NOTE: debate word data is in 3 files (dem, rep, rep undercard) because one file too bit for GitHub :(
with open("./test_code/debates_top_words_d.json") as debate_data_file_dem:
    debate_data_d = json.load(debate_data_file_dem)
    debate_data_file_dem.close() # democratic debates
with open("./test_code/debates_top_words_r.json") as debate_data_file_rep:
    debate_data_r = json.load(debate_data_file_rep)
    debate_data_file_rep.close() # republican debates
with open("./test_code/debates_top_words_r_u.json") as debate_data_file_rep_under:
    # republican undercard debates
    debate_data_r_u = json.load(debate_data_file_rep_under)
    debate_data_file_rep_under.close()
with open("./test_code/candidates_top_words.json") as candidate_data_file:
    candidate_data = json.load(candidate_data_file)
    candidate_data_file.close()
with open("./test_code/candidates_top_ten_words_tfidf.json") as candidate_top_words_file:
    candidate_top_ten_data = json.load(candidate_top_words_file)
    candidate_top_words_file.close()
with open("./test_code/candidate_responses.json") as candidate_response_file:
    candidate_responses = json.load(candidate_response_file)
    candidate_response_file.close()
with open("./test_code/candidates_which_debates.json") as candidate_which_debates:
    candidate_num_debates = json.load(candidate_which_debates)
    candidate_which_debates.close()

def search_candidate(query):
    try:
        top_ten_words = candidate_top_ten_data[query]

        # candidate responses
        responses = candidate_responses[query]

        return (top_ten_words, responses) 
    except KeyError:
        return {}, {}

def search_term(query):
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

		
def format_candidate_name(query):
#replaces the query word with the appropriate lowercase last name if any of these names exist in the query
	names = { 'clinton': ['hillary', 'clinton', 'hillary 	clinton','secretary clinton'],
			  'sanders': ['bernie','sanders','bernie sanders', 'senator sanders'],
			  "o'malley": ['martin', "o'malley","martin o'malley"],
			  'chafee': ['chafee', 'lincoln chafee'],
			  'webb': ['jim','webb','jim webb'],
			  'cruz': ['ted','cruz','ted cruz','senator cruz'],
			  'kasich': ['john','kasich','john kasich','governor kasich'],
			  'trump': ['donald','trump','donald trump'],
			  'rubio': ['marco','rubio','marco rubio','senator rubio'],
			  'carson': ['ben','carson','ben carson'],
			  'bush': ['jeb','bush','jeb bush'],
			  'christie': ['chris','christie','chris christie','governor christie'],
			  'fiorina': ['carly','fiorina','carly fiorina'],
			  'santorum': ['rick','santorum','rick santorum'],
			  'paul': ['rand','paul','rand paul','senator paul'],
			  'huckabee': ['mike','huckabee','mike huckabee','senator huckabee'],
			  'pataki': ['george','pataki','george pataki'],
			  'graham': ['lindsey','graham','lindsey graham','senator graham'],
			  'jindal': ['bobby','jindal','bobby jindal','governor jindal'],
			  'walker': ['scott','walker','scott walker','governor walker'],
			  'perry': ['rick','perry','rick perry']
			}
	thename = query
	for term in names.keys():
		for alt in names[term]:
			if query.lower() in alt:
				thename = term
	return thename