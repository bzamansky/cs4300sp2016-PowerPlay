# portions of code sourced from
# http://www.cs.cornell.edu/courses/cs4300/2016sp/Demos/demo20_2.html
from .test import debate_data_d, debate_data_r, debate_data_r_u
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize


class OurSVD(object):
    """Attributes:
    
    document_list: list of strings; each string is a document
    words_compressed: |V|*k matrix
    s: length-k diagonal matrix; the singular values
    docs_compressed: |D|*k matrix
    word_to_index: dict mapping vocab words to indices from 0 to |V|-1
    index_to_word: dict mapping indices to vocab words
    """
    def __init__(self, k, terms_per_doc=200):
        self.naive_parse(terms_per_doc)
        self.perform_svd_and_get_vocab(k)
    
    def naive_parse(self, terms_per_doc):
        """Goes through all of the words in all of the debates and naively
        splits them up into 'documents' of size `terms_per_doc`. Sets the
        document_list attribute."""
        giant_word_list = []
        
        all_debate_dicts = {}
        all_debate_dicts.update(debate_data_d)
        all_debate_dicts.update(debate_data_r)
        all_debate_dicts.update(debate_data_r_u)
        
        for debate_title, word_frequency_dict in all_debate_dicts.iteritems():
            for word, frequency in word_frequency_dict.iteritems():
                if len(word.split()) > 1:
                    continue  # no bigrams for this parsing
                giant_word_list.extend([word]*frequency)
        
        print len(giant_word_list)
        print 'negative one'
        random.shuffle(giant_word_list)  # so that a document isn't just the same word repeated over and over
        print 'zero'
        
        num_documents = len(giant_word_list) // terms_per_doc
        document_list = []
        
        for i in xrange(num_documents + 1):
            print num_documents - i
            document_list.append(
                ' '.join(giant_word_list[i*terms_per_doc:(i+1)*terms_per_doc])
            )
        
        self.document_list = document_list

    def perform_svd_and_get_vocab(self, k):
        """Sets the words_compressed, s, docs_compressed, word_to_index, and
        index_to_word attributes."""
        vectorizer = TfidfVectorizer(stop_words='english', min_df=10)
        print 'one'
        tfidf = vectorizer.fit_transform(self.document_list).transpose()
        print 'two'
        u, s, v_t = svds(tfidf, k)
        print 'three'
        self.words_compressed = normalize(abs(u), axis=1)  # row normalize
        self.s = s
        self.docs_compressed = v_t.transpose()
        
        self.word_to_index = vectorizer.vocabulary_
        self.index_to_word = {i:t for t,i in self.word_to_index.iteritems()}
    
    def test(self):
        pass