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
    values_interactions = None
    top_ten_words = None
    top_ten_words_counts = None
    respond_to = None
    respond_values = None
    # total_mentions_debate, total_mentions_candidate, interactions = None, None, None
    # top_ten, responses = None, None

    if request.GET.get('search'):
        search = request.GET.get('search').lower() # make case insensitive
        search_option = request.GET.get('search_option')
        opt1 = False
        opt2 = False
        if search_option=="candidate": opt1 = True
        if search_option=="term": opt2 = True
        
        # CHECK THIS: problem here? dunno...
        # if opt2 == True: # term
            # (total_mentions_debate, total_mentions_candidate, interactions) = search_results_term(search,opt1,opt2)
            # # # THIS IS BATYA'S MOSTLY WORKING CODE
            # # output = total_mentions_candidate
            # # candidates = total_mentions_candidate.keys()
            # # for i,k in enumerate(total_mentions_candidate.keys()):
            # #     cand_nums.append([k, total_mentions_candidate[k]])
            # # cand_nums.sort(key=lambda x: x[1], reverse=True)
            # values_by_candidate = total_mentions_candidate.values()
            # values_by_debate = total_mentions_debate.values()
            # debate_titles = total_mentions_debate.keys()
            # values_interactions = interactions.values()
        # elif opt1 == True: # candidate
            # (top_ten, responses) = search_results_candidate(search, opt1, opt2)
            # top_ten_words = top_ten.keys()
            # top_ten_words_counts = top_ten.values()
            # respond_to = responses.keys()
            # respond_values = responses.values()
            
        # print(type(output)) # make sure it's a dict for JsonResponse
        #http://stackoverflow.com/questions/30531990/matplotlib-into-a-django-template

        #(total_mentions_debate, total_mentions_candidate, interactions) = search_results_term(search,opt1,opt2)
        (total_mentions_debate, total_mentions_candidate, interactions) = search_results(search,opt1,opt2)
        #(top_ten, responses) = search_results_candidate(search, opt1, opt2)
        (top_ten, responses, dummy) = search_results(search, opt1, opt2)
        # print(top_ten)

        # THIS IS BATYA'S MOSTLY WORKING CODE
        output = total_mentions_candidate
        candidates = total_mentions_candidate.keys()
        for i,k in enumerate(total_mentions_candidate.keys()):
            cand_nums.append([k, total_mentions_candidate[k]])
        cand_nums.sort(key=lambda x: x[1], reverse=True)
        
        # with open('project_template/cand_hist_data.json','w') as outfile:
        #     json.dump(cand_nums, outfile)
        
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
        values_interactions = interactions.values()
        # top_ten_words = top_ten.keys()
        # top_ten_words_counts = top_ten.values()
        # respond_to = responses.keys()
        # respond_values = responses.values()

    return render_to_response('project_template/index.html', 
                          {'output': output,
                          'search_option_normal': search_option, # want to know if search by candidate or term
                          'search_option': json.dumps(search_option),
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
                           'interactions': values_interactions
                           })
    #                        'ten_words': json.dumps(top_ten_words),
    #                        'ten_words_counts': top_ten_words_counts,
    #                        'respond_names': json.dumps(respond_to),
    #                        'respond_values': respond_values
    # 