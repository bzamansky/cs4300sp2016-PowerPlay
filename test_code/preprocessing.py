import bs4, re, urllib3, time, os, json
import numpy as np
from sklearn.cross_validation import ShuffleSplit
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction import text 


candidates = [
  'clinton',
  'sanders',
  "o'malley",
  'chafee',
  'webb',
  'cruz',
  'kasich',
  'trump',
  'rubio',
  'carson',
  'bush',
  'christie',
  'fiorina',
  'santorum',
  'paul',
  'huckabee',
  'pataki',
  'graham',
  'jindal',
  'walker',
  'perry'
]

names = [
  'hillary',
  'clinton',
  'hillary clinton',
  'secretary clinton',
  'bernie',
  'sanders',
  'bernie sanders',
  'senator sanders',
  'martin',
  "o'malley",
  "martin o'malley",
  #'lincoln',
  'chafee',
  'lincoln chafee',
  'jim',
  'webb',
  'jim webb',
  'ted',
  'cruz',
  'ted cruz',
  'senator cruz',
  'john',
  'kasich',
  'john kasich',
  'governor kasich',
  'donald',
  'trump',
  'donald trump',
  'marco',
  'rubio',
  'marco rubio',
  'senator rubio',
  'ben',
  'carson',
  'ben carson',
  'jeb',
  'bush',
  'jeb bush',
  'chris',
  'christie',
  'chris christie',
  'governor christie',
  'carly',
  'fiorina',
  'carly fiorina',
  'rick',
  'santorum',
  'rick santorum',
  'rand',
  'paul',
  'rand paul',
  'senator paul',
  'mike',
  'huckabee',
  'mike huckabee',
  'senator huckabee',
  'george',
  'pataki',
  'george pataki',
  'lindsey',
  'graham',
  'lindsey graham',
  'senator graham',
  'bobby',
  'jindal',
  'bobby jindal',
  'governor jindal',
  'scott',
  'walker',
  'scott walker',
  'governor walker',
  'rick',
  'perry',
  'rick perry'
]
moderators = ["andrea","moderators", "hemmer", "gilmore", "maccallum", "dickerson", "cordes", "cooney", "obradovich", "cavuto", "bartiromo", "baker", "unknown", "ramos", "salinas ", "ramos ", "salinas", "tumulty", "question ", "question", "smith", "unknown [through translator", "unknown: ", "blitzer", "bash", "hewitt", "hannah debella, college student", "holt", "franchesca ramsey", "mitchell", "franta", "announcer", "brownlee", "tapper", " ", "tapper(?)", "unidentified male", "male", "regan", "cooper", "lemon", "kelly", "baier", "wallace", "", "...", "unidentified female", " kasich", "kasich: ", "moderator", "cuomo", "hannity", "unidentifiable", "woodruff", "ifill", "dinan", "quick", "harwood", "quintanilla", "cramer", "santelli", "epperson", "todd", "maddow", "strassel", "garrett", "audience", "wilkins", "lopez", "seib", "unidentified", "muir", "raddatz", "ham", "mcelveen", "o'connor", "josh jacob, college student", "louis", "audience member", "quick: ", "levesque", "???", "trump(?)", "cruz(?)", "arraras"]

additional_stops = ['people','time','mrs','long','ought','sure','new','thing','things','yes','no','think','know','just','want','lot','going','really','make','say','said','got','need','right','tell','like','ll','let','way','look','great','did']

with open("all_debate_list.json", "r") as f:
    transcripts = json.load(f)

speeches = [x['speech'] for x in transcripts]

## getting term-doc matrix
#ngram_range=(1, 2),
vectorizer = CountVectorizer(strip_accents='unicode',analyzer="word",lowercase=True, stop_words="english")  # for  unigrams only use ngram_range=(1, 1)
vectorizer.fit(speeches)

terms = vectorizer.get_feature_names()
#Document here is one line by a speaker, in any debate.
term_document_matrix = vectorizer.transform(speeches)

#Modifying stopwords
my_additional_stop_words = ['ve','don','t','um','uh']
stop_words = text.ENGLISH_STOP_WORDS.union(my_additional_stop_words)
stop_words = stop_words.union(moderators).union(additional_stops)

#Sorting the term-doc stuff by candidate

candidate_json = {}
#make each candidate a document, with everything they say jumbled into one


speeches_by_candidate = [""] * len(candidates)
candidates_to_index = {}
for i,candidate in enumerate(candidates):
  candidates_to_index[candidate] = i

for speech in transcripts:
  sp = speech['speaker']
  if sp in candidates:
    index = candidates_to_index[sp]
    speeches_by_candidate[index] += speech['speech']

with open("candidate_statements.json",'r') as f:
  s = json.load(f)
for x in s.keys():
  old_string = speeches_by_candidate[candidates_to_index[x]]
  new_string = " ".join(s[x])
  result_string = old_string + new_string
  speeches_by_candidate[candidates_to_index[x]] = result_string

#play with the max_df and min_df to get something we like.
#add ngram_range=(1,2) back to paramaters if we want them
c_vectorizer = CountVectorizer(strip_accents='unicode',analyzer="word",lowercase=True, stop_words=stop_words)
c_vectorizer.fit(speeches_by_candidate)
c_terms = c_vectorizer.get_feature_names()
candidate_term_matrix = c_vectorizer.transform(speeches_by_candidate)

#WE NEED TO STEM BECAUSE MEXICAN != MEXICANS

with open("debate_data.json", "r") as f:
  debates_list = json.load(f)

debates = []
debate_names = []
debates_to_index = {}
for i,d in enumerate(debates_list):
  debates_to_index[d['name']] = i
  debate_names.append(d['name'])
  tran = ""
  for x in d['tran']:
    tran += x['speech']
  debates.append(tran)
# total # of words
# x = 0
# for d in debates:
#   x += len(d.split(" "))
# print(x)

#ngram_range=(1,2),
d_vectorizer = CountVectorizer(strip_accents='unicode',analyzer="word",lowercase=True, stop_words=stop_words)
d_vectorizer.fit(debates)
d_terms = d_vectorizer.get_feature_names()
debate_term_matrix = d_vectorizer.transform(debates)

def most_spoken_words_by_candidate(candidate,n=10):
  cand_array = candidate_term_matrix.toarray()
  can_row = candidates_to_index[candidate]
  words = cand_array[can_row]
  top = sorted(range(len(words)), key=lambda i: words[i], reverse=True)[:n]
  top_words = {}
  for x in top:
    top_words[c_terms[x]] = cand_array[can_row,x]
  return top_words

def most_spoken_words_by_debate(debate,n=10):
  deb_array = debate_term_matrix.toarray()
  deb_row = debates_to_index[debate]
  words = deb_array[deb_row]
  top = sorted(range(len(words)), key=lambda i: words[i], reverse=True)[:n]
  top_words = {}
  for x in top:
    top_words[d_terms[x]] = deb_array[deb_row,x]
  return top_words

def word_spoken_most_by_candidate(word,n=10):
  cand_array = candidate_term_matrix.toarray()
  word_ind = c_terms.index(word)
  word_col = cand_array[:,word_ind]
  top = sorted(range(len(word_col)), key=lambda i: word_col[i], reverse=True)[:n]
  top_candidates = []
  for x in top:
    top_candidates.append((candidates[x],cand_array[x,word_ind]))
  return top_candidates


candidates_top_words = {}
for c in candidates:
  candidates_top_words[c] = most_spoken_words_by_candidate(c,len(c_terms))

with open('candidates_top_words.json','w') as outfile:
  json.dump(candidates_top_words, outfile, sort_keys=True, indent=4, separators=(',', ': '))

debates_top_words_d = {}
debates_top_words_r = {}
debates_top_words_r_u = {}
for d in debate_names:
  party = d.split(" ")[-1]
  und = d.split(" ")[-2]
  if party == "D":
    debates_top_words_d[d] = most_spoken_words_by_debate(d,len(d_terms))
  elif und == "U":
    debates_top_words_r_u[d] = most_spoken_words_by_debate(d,len(d_terms))
  else:
    debates_top_words_r[d] = most_spoken_words_by_debate(d,len(d_terms))

with open('debates_top_words_d.json','w') as outfile:
  json.dump(debates_top_words_d, outfile, sort_keys=True, indent=4, separators=(',', ': '))

with open('debates_top_words_r.json','w') as outfile:
  json.dump(debates_top_words_r, outfile, sort_keys=True, indent=4, separators=(',', ': '))

with open('debates_top_words_r_u.json','w') as outfile:
  json.dump(debates_top_words_r_u, outfile, sort_keys=True, indent=4, separators=(',', ': '))


candidate_responses = {}
for c in candidates:
  candidate_responses[c] = {}
  for c2 in candidates:
    if c2 != c:
      candidate_responses[c][c2] = 0
for line in transcripts:
  if line['prev'] in candidates:
    candidate_responses[line['speaker']][line['prev']] += 1

with open('candidate_responses.json','w') as outfile:
  json.dump(candidate_responses, outfile, sort_keys=True, indent=4, separators=(',',': '))

ct_vectorizer = TfidfVectorizer(strip_accents='unicode',analyzer="word",lowercase=True, stop_words=stop_words)
ct_vectorizer.fit(speeches_by_candidate)
ct_terms = ct_vectorizer.get_feature_names()
candidate_term_t_matrix = ct_vectorizer.transform(speeches_by_candidate)

def most_spoken_words_by_candidate_tfidf(candidate,n=10):
  cand_array = candidate_term_t_matrix.toarray()
  can_row = candidates_to_index[candidate]
  words = cand_array[can_row]
  top = sorted(range(len(words)), key=lambda i: words[i], reverse=True)[:n]
  top_words = {}
  for x in top:
    if x < len(ct_terms):
      top_words[ct_terms[x]] = cand_array[can_row,x]
  return top_words

candidates_top_ten_words_tfidf = {}
for c in candidates:
  candidates_top_ten_words_tfidf[c] = most_spoken_words_by_candidate_tfidf(c)

with open('candidates_top_ten_words_tfidf.json', 'w') as outfile:
  json.dump(candidates_top_ten_words_tfidf, outfile, sort_keys=True, indent=4, separators=(',',': '))

candidates_top_ten_words = {}
for c in candidates:
  candidates_top_ten_words[c] = most_spoken_words_by_candidate(c)

with open('candidates_top_ten_words.json', 'w') as outfile:
  json.dump(candidates_top_ten_words, outfile, sort_keys=True, indent=4, separators=(',',': '))


cand_top_ten_snippits = candidates_top_ten_words_tfidf

def snippits(word,candidate):
  span = 15
  outputs = []
  ind = candidates_to_index[candidate]
  text = speeches_by_candidate[ind].split(" ")
  indices = [i for i,x in enumerate(text) if x == word or x == word.title()]
  if len(indices) < 4:
    indices = indices
  else:
    indices = indices[:4]
  for x in indices:
    if x > span and x < len(text) - span:
      low = x - span
      high = x + span
      output_str = text[low:high]
      s = "..." + " ".join(output_str) + "..."
      if s in outputs:
        continue
      outputs.append(s)
  return outputs

for c in cand_top_ten_snippits.keys():
  for w in cand_top_ten_snippits[c].keys():
    cand_top_ten_snippits[c][w] = snippits(w,c)

with open('cand_top_ten_snippits.json','w') as outfile:
  json.dump(cand_top_ten_snippits, outfile, sort_keys=True, indent=4, separators=(',',': '))
