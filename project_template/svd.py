# portions of code sourced from
# http://www.cs.cornell.edu/courses/cs4300/2016sp/Demos/demo20_2.html
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import json
import numpy as np

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
MORE_STOPS = ['ve','don','t','um','uh']
EVEN_MORE_STOPS = [
    'people','time','mrs','long','ought','sure','new','thing','things','yes',
    'no','think','know','just','want','lot','going','really','make','say',
    'said','got','need','right','tell','like','ll','let','way','look','great',
    'did'
]
ALL_OUR_STOP_WORDS = list(ENGLISH_STOP_WORDS) + MORE_STOPS + EVEN_MORE_STOPS


class OurSVD(object):
    """Attributes:
    
    document_list: list of strings; each string is a document
    words_compressed: |V|*k matrix
    s: length-k diagonal matrix; the singular values
    docs_compressed: |D|*k matrix
    word_to_index: dict mapping vocab words to indices from 0 to |V|-1
    index_to_word: dict mapping indices to vocab words
    """
    def __init__(self, candidate=None, k=20, terms_per_doc=150):
        """If `candidate` is None, gets topics for all of the debate speeches
        combined; otherwise only gets topics for that candidate's speeches"""
        self._naive_parse(candidate, terms_per_doc)
        self._perform_svd_and_get_vocab(k)
        
    def _naive_parse(self, candidate, terms_per_doc):
        """Goes through all of the words in all of the relevant debates, in
        order, and naively splits them up into sequential 'documents' of size
        `terms_per_doc`. Sets the document_list attribute.
        
        Cannot just use or reuse a vectorizer here since word order is highly
        important.
        """
        with open("test_code/all_debate_list.json") as f:
            transcripts = json.load(f)
        if not candidate:
            speeches = [s['speech'] for s in transcripts]
        else:
            speeches = [
                s['speech'] for s in transcripts if s['speaker'] == candidate
            ]
        giant_word_list = ' '.join(speeches).split()
        
        num_documents = len(giant_word_list) // terms_per_doc
        document_list = []
        
        for i in xrange(num_documents + 1):
            document_list.append(
                ' '.join(giant_word_list[i*terms_per_doc:(i+1)*terms_per_doc])
            )
        
        self.document_list = document_list

    def _perform_svd_and_get_vocab(self, num_topics):
        """Sets the words_compressed, s, docs_compressed, word_to_index, and
        index_to_word attributes."""
        vectorizer = TfidfVectorizer(stop_words=ALL_OUR_STOP_WORDS)
        tfidf = vectorizer.fit_transform(self.document_list).transpose()
        u, s, v_t = svds(tfidf, num_topics)
        self.words_compressed = abs(u)
        self.s = s
        self.docs_compressed = v_t.transpose()
        
        self.word_to_index = vectorizer.vocabulary_
        self.index_to_word = {i:t for t,i in self.word_to_index.iteritems()}
    
    def closest_words(self, input, n=10):
        """Takes a string input and attempts to parse it as a sequence of words.
        Returns TWO lists:
        a list of up to `n` words that are closest in meaning to the input
        word(s), and list of words that failed to be parsed because they were
        not in the vocab (makes error handling easy for the caller)."""
        raw_words = input.split()
        if not raw_words:
            return [], [input]  # no result due to blank input
        
        # I have got to stop leaking 3110 into this code
        good_words = [w for w in raw_words if w in self.word_to_index]
        bad_words = [w for w in raw_words if w not in self.word_to_index]
        
        if not good_words:
            return [], bad_words  # no result due to all words not found
        
        # use normalized rows from this point onward
        normalized_words_compressed = normalize(self.words_compressed, axis=1)
        
        # if multiple terms searched, average their *normalized* rows
        u_row_sum = np.copy(
            normalized_words_compressed[self.word_to_index[good_words[0]],:]
        )
        for w in good_words[1:]:
            u_row_sum = normalized_words_compressed[self.word_to_index[w],:]
        
        sims = normalized_words_compressed.dot(u_row_sum)
        asort = np.argsort(-sims)
        # word(s) may be most similar to itself/themselves; remove
        asort = list(asort)
        for w in good_words:
            index = self.word_to_index[w]
            asort.remove(index)
        return [(self.index_to_word[i]) for i in asort[:n]], bad_words
    
    def get_topics_readable(self, n=10):
        """Returns the top `n` words of all k topics found by this SVD, as a
        list of k lists of `n` strings."""
        topics = []
        k = self.s.shape[0]
        for i in range(k):
            topics.append(np.argsort(self.words_compressed[:,i])[::-1])
        readable_topics = []
        for t in topics:
            readable_topics.append(
                [self.index_to_word[vocab_index] for vocab_index in t[:n]]
            )
        return readable_topics
