from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
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
    cand_nums=[]
    new_file_path = ''
    candidates = None
    values_by_candidate = None
    values_by_debate = None
    debate_titles = None
    values_interactions = None

    if request.GET.get('search'):
        search = request.GET.get('search').lower() # make case insensitive
        search_option = request.GET.get('search_option')
        opt1 = False
        opt2 = False
        if search_option=="candidate": opt1 = True
        if search_option=="term": opt2 = True
        (total_mentions_debate, total_mentions_candidate, interactions) = search_results(search,opt1,opt2)
        output = total_mentions_candidate
        # print(type(output)) # make sure it's a dict for JsonResponse
        #http://stackoverflow.com/questions/30531990/matplotlib-into-a-django-template

        # THIS IS BATYA'S MOSTLY WORKING CODE
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

    return render_to_response('project_template/index.html', 
                          {'output': output,
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
    