import bs4
import re
#import requests
import time
import os
import json

#This is the scraping data!

# File containing all the links to the debates
# all_debates_filename = "Presidential_Debates.html"
# with open(all_debates_filename) as f:
#   all_debates = bs4.BeautifulSoup(f)

# #Manually found the table that has the debate data
# table = all_debates.find_all('table',{'class':'TABLE_WE_NEED'})
# #Getting all rows of the debate table to get the links
# links = table[0].find_all('tr')
# all_debates = []
# for row in links:
#   #The date of the debate
#   dates = row.find_all('td',{'class':'docdate'})
#   if len(dates) == 0:
#     continue
#   date = dates[0].text
#   sep_date = date.split(', ')
#   #We only want 2015-2016 debate data for simplicity
#   if len(sep_date) != 2 or int(sep_date[1]) < 2015:
#     continue
#   #Get the links to the debates
#   debates = row.find_all('td',{'class':'doctext'})
#   #If the debate hasn't happened yet, skip this row
#   if len(debates) == 0:
#     continue
#   debate = debates[0]
#   debate_links = debate.find('a')
#   if not debate_links:
#     continue
#   link = debate_links['href']
#   #Put the debate data into a list of links to follow
#   all_debates.append({'date':date,'debate':debate.text,'link':link})

# transcript_files = []
# #Working through the debate links and pulling the file
# for d in all_debates:
#   http = urllib3.PoolManager()
#   r = http.request('GET', d['link'])
#   if r.status != 200:
#     break
#   file = bs4.BeautifulSoup(r.data)
#   file_name = file.find_all('span',{'class':'paperstitle'})[0].text
#   name_spl = file_name.split()
#   spl = name_spl.index('in')
#   place = "_".join(name_spl[spl:])
#   name = os.path.join('debates',("_".join(name_spl) + ".html"))
#   #Writing the debate to a new file to keep from scraping the website too many times
#   fo = open(name,"wb")
#   fo.write(r.data)
#   fo.close()
#   time.sleep(5)

transcripts = []
moderators = []
#Manually listing candidates
candidates = [
  'clinton',
  'sanders',
  "o'malley",
  'chafee',
  'webb',
  'cruz',
  'kasich',
  'trump',
  'rubio',
  'carson',
  'bush',
  'christie',
  'fiorina',
  'santorum',
  'paul',
  'huckabee',
  'pataki',
  'graham',
  'jindal',
  'walker',
  'perry'
]

# normalize
candidate_which_debates = {}
for c in candidates:
  candidate_which_debates[c] = []


#Going through the folder of downloaded debates
for file in os.listdir('debates'):
  transcript_filename = os.path.join('debates',file)
  transcript = {"file":transcript_filename}
  with open(transcript_filename) as f:
    bsoup = bs4.BeautifulSoup(f)

  #Grabbed the file, souping it
  tran = bsoup.find_all('span',{'class':'displaytext'})
  
  #Date of the debate
  date = bsoup.find_all('span',{'class':'docdate'})
  transcript['date'] = date[0].text
  date = date[0].text
  #Debate information
  debate = file.strip(".html")
  party = debate.split("_")[0]
  debate_loc_words = debate.split("_")
  loc = " ".join(debate_loc_words[2:])
  name = date + " " + " ".join(loc.split(" ")[2:])
  if 'Undercard' in debate_loc_words:
    name += " U"
  if party == "Democratic":
    name += " D"
  if party == "Republican":
    name += " R"

  transcript['name'] = name

  #Getting each line of the debate
  pars = tran[0].find_all('p')

  parsed = []

  curr_speaker = ''
  #Parsing each line in the debate
  for i,x in enumerate(pars):
    prev = ''
    t = re.sub('\[.*\]','',x.text) # line to cut out [applause] lines
    t = re.sub(ur'\u2014','-',t,re.UNICODE) #line to make em-dashes into single dashes
    t = re.sub(ur'\u00e1','a',t,re.UNICODE) #take out accented a
    t = re.sub(ur'\u00c1','a',t,re.UNICODE) #take out accented A
    mod = False #Automatically saying the speaker is not a moderator
    if x.b:
      speaker = re.sub('\[.*\]','',x.b.text) #take out [applause] and other things in brackets
      #Removing the speaker from the beginning of the line
      if t.startswith(speaker):
        t = t[len(speaker):]
      speaker = re.sub(ur'\u00ed','i',speaker,re.UNICODE) #take out accented I #take out accented A
      speaker = re.sub(ur'\u00c1','A',speaker,re.UNICODE) #take out accented A

      #Lowercase the speaker to match to a candidate
      tmp_speaker = str(speaker.encode('utf8').lower()).strip(":")
      #If the speaker isn't a candidate, they are a 'moderator' for our purposes
      if tmp_speaker not in candidates:
        mod = True
        if tmp_speaker not in moderators:
          moderators.append(tmp_speaker)
      elif tmp_speaker not in candidates and tmp_speaker not in moderators:
        candidates.append(tmp_speaker)
      speaker = speaker.strip(":").lower()
      if curr_speaker != speaker:
        if not mod and speaker not in moderators:
          prev = curr_speaker
        curr_speaker = speaker
      parsed.append({'speaker':speaker,'speech':t, 'date':date, 'moderator':mod,'party':party,'location':loc, 'prev':prev})
      if speaker in candidates:
        if name not in candidate_which_debates[speaker]:
          candidate_which_debates[speaker].append(name)
    else:
      #Add the text to the speaker
      parsed[-1]['speech'] = parsed[-1]['speech'] + t

  #Add this transcript to the list of transcripts
  transcript['tran'] = parsed
  transcripts.append(transcript)

#Removing the moderator's stuff because file space
actual_transcripts = []
# all_words = []
# x = 0
for tran in transcripts:
  actual_tran = {'date':tran['date'],'file':tran['file'],'name':tran['name'],'tran':[]}
  for file in tran['tran']:
    # words = file['speech'].split(" ")
    # x += len(words)
    # all_words.extend(words)
    if file['speaker'] in candidates:
      actual_tran['tran'].append(file)
  actual_transcripts.append(actual_tran)
# print(x)
# print(len(set(all_words)))
# print(actual_transcripts)

#Dump all the debates into a json file for ease of access
with open('debate_data.json', 'w') as outfile:
    json.dump(actual_transcripts, outfile, sort_keys=True, indent=4, separators=(',', ': '))

#Dump all the debates into one single list and into another document
all_debate_list = []
for x in actual_transcripts:
  all_debate_list = all_debate_list + x['tran']

with open('all_debate_list.json','w') as outfile:
  json.dump(all_debate_list, outfile, indent=4, separators=(',', ': '))

# Dump candidates_which_debate into json file to read which debates each candidate participated in
with open('candidates_which_debates.json', 'w') as outfile:
  json.dump(candidate_which_debates, outfile, indent=4, separators=(',', ': '))

