from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import search_candidate
from .test import search_term
from .test import format_candidate_name
from django.contrib.staticfiles.templatetags.staticfiles import static
import json
from .svd import OurSVD


def index(request):
    output_list = ''
    output=''
    search = ''
    search_option = ''
    new_file_path = ''
    candidates = None
    values_by_candidate = None
    values_by_debate = None
    debate_titles = None
    top_ten = None
    respond_to = None
    respond_values = None
    all_debate_text = None
    num_debates = None
    snippits = None
    candidate_info = None
    closest_words, error_words = None, None
    adjusted = ''
    thequery = ''
    num_debates = None  # this is where the normalization begins
    topics = None
    
    
    if 'search' in request.GET:
        search = request.GET['search'].lower().strip()  # make case insensitive
        search_option = request.GET.get('search_option')
        eval_type = request.GET.get('eval')
        top_ten = None
        responses = None
        total_mentions_debate = None
        total_mentions_candidate = None

        if search_option == 'candidate':
            thequery = search
            adjusted = format_candidate_name(search)
            top_ten, responses = search_candidate(adjusted)
            top_ten_words = top_ten.keys()
            top_ten_words_counts = top_ten.values()
            respond_to = responses.keys()
            respond_values = responses.values()
            
            # do not attempt to construct SVD on nonexistent candidate search
            if eval_type == 'ml' and top_ten:
                this_candidates_svd = OurSVD(adjusted, k=10)
                topics = this_candidates_svd.get_topics_readable()
            
        else: #if search_option == 'term'
            thequery = search
            total_mentions_debate, total_mentions_candidate, candidate_num_debates = search_term(search)
            num_debates = candidate_num_debates
            
            if eval_type == 'ml':
                our_svd = OurSVD()  # default params passed to constructor
                closest_words, error_words = our_svd.closest_words(search)
                
                for word in closest_words:
                  (tmp_total_debates,tmp_total_mentions,_) = search_term(word)
                  for k in tmp_total_mentions.keys():
                    total_mentions_candidate[k] += tmp_total_mentions[k]
                  for k in tmp_total_debates.keys():
                    total_mentions_debate[k] += tmp_total_debates[k]
            elif eval_type == 'naive':
                if not total_mentions_debate:
                    error_words = [search]

            candidates = total_mentions_candidate.keys()
            values_by_candidate = total_mentions_candidate.values()
            values_by_debate = total_mentions_debate.values()
            debate_titles = total_mentions_debate.keys()
        
        with open("./test_code/cand_top_ten_snippits.json") as snippits_file:
            snippits = json.load(snippits_file)
            snippits_file.close()
        with open("./test_code/candidate_info.json") as candidate_info_file:
            candidate_info = json.load(candidate_info_file)
            candidate_info_file.close()
        return render_to_response('project_template/index.html', 
                          {'search_option': search_option,
                           'adjustedsearch': '"'+ adjusted +'"',
                           'searched': thequery,
                           'candidate_names': json.dumps(candidates),
                           'mentions_by_candidate': json.dumps(values_by_candidate),
                           'debate_titles': json.dumps(debate_titles),
                           'mentions_by_debate': json.dumps(values_by_debate),
                           'ten_words': json.dumps(top_ten),
                           'respond_names': json.dumps(respond_to),
                           'respond_values': json.dumps(respond_values),
                           'all_debates':json.dumps(snippits),
                           'num_debates':json.dumps(num_debates),
                           'closest_words': closest_words,
                           'related_terms': json.dumps(closest_words),
                           'error_words': error_words,
                           'eval_type':eval_type,
                           'eval':json.dumps(eval_type),
                           'suggested_candidates': ['clinton', 'sanders', 'trump', 'cruz', 'kasich'],
                           'suggested_terms': ['immigration', 'health', 'education'],
						   'candidate_info': json.dumps(candidate_info),
                           'topics': topics,
                           })
    # suggest terms/candidates to search for on the homepage
    else:
        return render_to_response('project_template/index.html', 
                          {'suggested_candidates': ['clinton', 'sanders', 'trump', 'cruz', 'kasich'],
                           'suggested_terms': ['immigration', 'health', 'education'],
                           'check_homepage': 'yes',  # yes it's the homepage
                          })
