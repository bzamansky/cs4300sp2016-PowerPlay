import bs4, re, urllib3, time, os, json
import numpy as np
from sklearn.cross_validation import ShuffleSplit
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report, confusion_matrix

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

with open("all_debate_list.json", "r") as f:
    transcripts = json.load(f)

speeches = [x['speech'] for x in transcripts]

## getting term-doc matrix
vectorizer = CountVectorizer(ngram_range=(1, 2),strip_accents='unicode',analyzer="word",lowercase=True, stop_words="english")  # for  unigrams only use ngram_range=(1, 1)
vectorizer.fit(speeches)

terms = vectorizer.get_feature_names()
#Document here is one line by a speaker, in any debate.
term_document_matrix = vectorizer.transform(speeches)

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

#play with the max_df and min_df to get something we like.
c_vectorizer = CountVectorizer(ngram_range=(1,2),strip_accents='unicode',analyzer="word",lowercase=True, stop_words="english")
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
  debates_to_index[d['file']] = i
  debate_names.append(d['file'])
  tran = ""
  for x in d['tran']:
    tran += x['speech']
  debates.append(tran)

d_vectorizer = CountVectorizer(ngram_range=(1,2),strip_accents='unicode',analyzer="word",lowercase=True, stop_words="english")
d_vectorizer.fit(debates)
d_terms = d_vectorizer.get_feature_names()
debate_term_matrix = d_vectorizer.transform(debates)

def most_spoken_words_by_candidate(candidate,n=10):
  cand_array = candidate_term_matrix.toarray()
  can_row = candidates_to_index[candidate]
  words = cand_array[can_row]
  top = sorted(range(len(words)), key=lambda i: words[i], reverse=True)[:n]
  top_words = []
  for x in top:
    top_words.append((c_terms[x],cand_array[can_row,x]))
  return top_words

def most_spoken_words_by_debate(debate,n=10):
  deb_array = debate_term_matrix.toarray()
  deb_row = debates_to_index[debate]
  words = deb_array[deb_row]
  top = sorted(range(len(words)), key=lambda i: words[i], reverse=True)[:n]
  top_words = []
  for x in top:
    top_words.append((d_terms[x],deb_array[deb_row,x]))
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
