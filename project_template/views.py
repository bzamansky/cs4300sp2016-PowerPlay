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
    values = None
    if request.GET.get('search'):
        search = request.GET.get('search')
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


        # https://docs.djangoproject.com/en/dev/ref/request-response/#jsonresponse-objects
        # save json data to file, open this file using javascript in index.html
        # new_file_path = static('output_data_file.json')
        # print("hi"+new_file_path)
        # data = str(output)
        # with open(new_file_path,'w') as outfile:
        #     json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

        values = total_mentions_candidate.values()

    return render_to_response('project_template/index.html', 
                          {'output': output,
                          # THIS IS BATYA'S MOSTLY WORKING CODE
                          'plot': cand_nums,
                          'searched': search,
                          # 'new_data_path': new_file_path,
                           'magic_url': request.get_full_path(),
                           # JACKIE CODE
                           'candidate_names': candidates,
                           'mentions': values
                           })
    