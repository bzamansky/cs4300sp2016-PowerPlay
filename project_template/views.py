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

# Create your views here.
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
    top_ten_words = None
    top_ten_words_counts = None
    respond_to = None
    respond_values = None
    all_debate_text = None
    num_debates = None
    snippits = None


    if 'search' in request.GET:
        search = request.GET['search'].lower() # make case insensitive
        search_option = request.GET.get('search_option')
        top_ten = None
        responses = None
        total_mentions_debate = None
        total_mentions_candidate = None
        candidate_num_debates = None

        if search_option == 'candidate':
          thequery = search
          adjusted = format_candidate_name(search)
          (top_ten, responses) = search_candidate(adjusted)
          top_ten_words = top_ten.keys()
          top_ten_words_counts = top_ten.values()
          respond_to = responses.keys()
          respond_values = responses.values()

        else: #if search_option == 'term'
          (total_mentions_debate, total_mentions_candidate, candidate_num_debates) = search_term(search)
          candidates = total_mentions_candidate.keys()
          values_by_candidate = total_mentions_candidate.values()
          values_by_debate = total_mentions_debate.values()
          debate_titles = total_mentions_debate.keys()
          num_debates_names = candidate_num_debates.keys()
          num_debates_values = candidate_num_debates.values()        

        with open("./test_code/cand_top_ten_snippits.json") as snippits_file:
            snippits = json.load(snippits_file)
            snippits_file.close()

    return render_to_response('project_template/index.html', 
                          {'search_option': search_option,
                           'adjustedsearch': '"'+ adjusted +'"',
                           'searched': thequery,
                           'candidate_names': json.dumps(candidates),
                           'mentions_by_candidate': json.dumps(values_by_candidate),
                           'debate_titles': json.dumps(debate_titles),
                           'mentions_by_debate': json.dumps(values_by_debate),
                           'ten_words': json.dumps(top_ten_words),
                           'ten_words_counts': top_ten_words_counts,
                           'respond_names': json.dumps(respond_to),
                           'respond_values': json.dumps(respond_values),
                           'all_debates':json.dumps(snippits)
                           })
