from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import search_candidate
from .test import search_term
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
    all_candidates = None
    num_debates = None


    if 'search' in request.GET:
        search = request.GET['search'].lower() # make case insensitive
        search_option = request.GET.get('search_option')
        top_ten = None
        responses = None
        total_mentions_debate = None
        total_mentions_candidate = None
        candidate_num_debates = None

        if search_option == 'candidate':
          (top_ten, responses) = search_candidate(search)
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

        all_candidates = ['clinton','sanders',"o'malley",'chafee','webb','cruz','kasich','trump','rubio','carson','bush','christie','fiorina','santorum','paul','huckabee','pataki','graham','jindal','walker','perry']

        candidate_to_i = {}
        for i,x in enumerate(all_candidates):
          candidate_to_i[x] = i
        with open('./test_code/all_debate_list.json') as all_debate_list_file:
          all_debate_list = json.load(all_debate_list_file)
          all_debate_list_file.close()
        all_debate_text = [""] * len(all_candidates)
        for x in all_debate_list:
          if x['speaker'] not in all_candidates:
            continue
          all_debate_text[candidate_to_i[x['speaker']]] += x['speech'].encode('ascii','ignore')
        with open('./test_code/candidate_statements.json') as statement_file:
          statements = json.load(statement_file)
          statement_file.close()
        for x in statements.keys():
          s = " ".join(statements[x])
          all_debate_text[candidate_to_i[x]] += s.encode('ascii','ignore')
    return render_to_response('project_template/index.html', 
                          {'search_option': search_option,
                          'searched': search,
                           'candidate_names': json.dumps(candidates),
                           'mentions_by_candidate': json.dumps(values_by_candidate),
                           'debate_titles': json.dumps(debate_titles),
                           'mentions_by_debate': json.dumps(values_by_debate),
                           'ten_words': json.dumps(top_ten_words),
                           'ten_words_counts': top_ten_words_counts,
                           'respond_names': json.dumps(respond_to),
                           'respond_values': json.dumps(respond_values),
                           'all_debates':json.dumps(all_debate_text),
                           'all_candidates':json.dumps(all_candidates)
                           })
