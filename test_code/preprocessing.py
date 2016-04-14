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
vectorizer = CountVectorizer(ngram_range=(1, 2),strip_accents='unicode')  # for  unigrams only use ngram_range=(1, 1)
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


c_vectorizer = CountVectorizer(ngram_range=(1,2),strip_accents='unicode',analyzer="word",lowercase=True)
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

d_vectorizer = CountVectorizer(ngram_range=(1,2),strip_accents='unicode',analyzer="word",lowercase=True)
d_vectorizer.fit(debates)
d_terms = d_vectorizer.get_feature_names()
debate_term_matrix = d_vectorizer.transform(debates)





print(d_terms.index('immigration'))
print(d_terms[62800])
print(debate_names)
print(debate_term_matrix.toarray()[:,62800])