from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
# COME BACK TO THIS
#from .test import search_results_candidate, search_results_term
from .test import search_results
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.staticfiles.templatetags.staticfiles import static
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

# Create your views here.
def index(request):
    output_list = ''
    output=''
    search = ''
    search_option = ''
    cand_nums = []
    new_file_path = ''
    candidates = None
    values_by_candidate = None
    values_by_debate = None
    debate_titles = None
    #values_interactions = None
    top_ten_words = None
    top_ten_words_counts = None
    respond_to = None
    respond_values = None
    all_debate_text = None
    all_candidates = None
    num_debates = None
    # total_mentions_debate, total_mentions_candidate, interactions = None, None, None
    # top_ten, responses = None, None

    if 'search' in request.GET:
        search = request.GET['search'].lower() # make case insensitive
        search_option = request.GET.get('search_option')
        
        #(total_mentions_debate, total_mentions_candidate, interactions) = search_results_term(search, search_option)
        (total_mentions_debate, total_mentions_candidate, candidate_num_debates) = search_results(search, search_option)
        #(top_ten, responses) = search_results_candidate(search, search_option)
        (top_ten, responses, dummy) = search_results(search, search_option)
        # print(top_ten)

        # THIS IS BATYA'S MOSTLY WORKING CODE
        output = total_mentions_candidate
        candidates = total_mentions_candidate.keys()
        for i,k in enumerate(total_mentions_candidate.keys()):
            cand_nums.append([k, total_mentions_candidate[k]])
        cand_nums.sort(key=lambda x: x[1], reverse=True)
      
        
        # paginator = Paginator(output_list, 10)
        # page = request.GET.get('page')
        # try:
        #     output = paginator.page(page)
        # except PageNotAnInteger:
        #     output = paginator.page(1)
        # except EmptyPage:
        #     output = paginator.page(paginator.num_pages)



        values_by_candidate = total_mentions_candidate.values()
        values_by_debate = total_mentions_debate.values()
        debate_titles = total_mentions_debate.keys()
        num_debates_names = candidate_num_debates.keys()
        num_debates_values = candidate_num_debates.values()
        #values_interactions = interactions.values()
        top_ten_words = top_ten.keys()
        top_ten_words_counts = top_ten.values()
        respond_to = responses.keys()
        respond_values = responses.values()

        all_candidates = ['clinton','sanders',"o'malley",'chafee','webb','cruz','kasich','trump','rubio','carson','bush','christie','fiorina','santorum','paul','huckabee','pataki','graham','jindal','walker','perry']

        candidate_to_i = {}
        for i,x in enumerate(all_candidates):
          candidate_to_i[x] = i
        all_debate_list_file = open('./test_code/all_debate_list.json')
        all_debate_list = json.load(all_debate_list_file)
        all_debate_text = [""] * len(all_candidates)
        for x in all_debate_list:
          if x['speaker'] not in all_candidates:
            continue
          all_debate_text[candidate_to_i[x['speaker']]] += x['speech'].encode('ascii','ignore')
        statement_file = open('./test_code/candidate_statements.json')
        statements = json.load(statement_file)
        for x in statements.keys():
          s = " ".join(statements[x])
          all_debate_text[candidate_to_i[x]] += s.encode('ascii','ignore')
    return render_to_response('project_template/index.html', 
                          {'output': output,
                          'search_option': search_option,
                          # THIS IS BATYA'S MOSTLY WORKING CODE
                          'plot': cand_nums,
                          'searched': search,
                          # 'new_data_path': new_file_path,
                           'magic_url': request.get_full_path(),
                           # JACKIE CODE
                           'candidate_names': json.dumps(candidates),
                           'mentions_by_candidate': values_by_candidate,
                           'debate_titles': json.dumps(debate_titles),
                           'mentions_by_debate': values_by_debate,
                           'ten_words': json.dumps(top_ten_words),
                           'ten_words_counts': top_ten_words_counts,
                           'respond_names': json.dumps(respond_to),
                           'respond_values': respond_values,
                           'candidate_num_debates_names': json.dumps(num_debates_names),
                           'candidate_num_debates:': num_debates_values,
                           'all_debates':all_debate_text,
                           'all_candidates':all_candidates
                           })
                          #'interactions': values_interactions,

