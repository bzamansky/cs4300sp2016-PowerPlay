from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
from .test import search_results
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
    output_list = ''
    output=''
    if request.GET.get('search'):
        search = request.GET.get('search')
        cand = request.GET.get('search_option_1')
        term = request.GET.get('search_option_2')
        opt1 = False
        opt2 = False
        if cand: opt1 = True
        if term: opt2 = True
        (total_mentions_debate, total_mentions_candidate, interactions) = search_results(search,opt1,opt2)
        output = total_mentions_candidate

        #http://stackoverflow.com/questions/30531990/matplotlib-into-a-django-template

        candidates = total_mentions_candidate.keys()
        cand_nums = []
        for i,k in enumerate(total_mentions_candidate.keys()):
            cand_nums.append(total_mentions_candidate[k])

        N = len(candidates)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.7       # the width of the bars

        fig = plt.figure()
        ax = fig.add_subplot(111)
        rects1 = ax.bar(ind, cand_nums, width, color='b')

        # add some text for labels, title and axes ticks
        ax.set_ylabel('Number of times said')
        ax.set_title('Candidates')
        ax.set_xticks(ind + width/2.)
        ax.set_xticklabels(candidates)


        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        '%d' % int(height),
                        ha='center', va='bottom')

        autolabel(rects1)
        #plt.show()
        plt.savefig('project_template/templates/project_template/candidates_plot')

        plot = 'project_template/templates/project_template/candidates_plot.png'
        # paginator = Paginator(output_list, 10)
        # page = request.GET.get('page')
        # try:
        #     output = paginator.page(page)
        # except PageNotAnInteger:
        #     output = paginator.page(1)
        # except EmptyPage:
        #     output = paginator.page(paginator.num_pages)
    return render_to_response('project_template/index.html', 
                          {'output': output,
                          'plot':plot,
                           'magic_url': request.get_full_path()
                           })