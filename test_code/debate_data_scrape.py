import bs4
import re
import urllib3
import time
import os
import json

#This is the scraping data!


# all_debates_filename = "Presidential_Debates.html"
# with open(all_debates_filename) as f:
#   all_debates = bs4.BeautifulSoup(f)

# table = all_debates.find_all('table',{'class':'TABLE_WE_NEED'})
# links = table[0].find_all('tr')
# all_debates = []
# for row in links:
#   dates = row.find_all('td',{'class':'docdate'})
#   if len(dates) == 0:
#     continue
#   date = dates[0].text
#   sep_date = date.split(', ')
#   if len(sep_date) != 2 or int(sep_date[1]) < 2015:
#     continue
#   debates = row.find_all('td',{'class':'doctext'})
#   if len(debates) == 0:
#     continue
#   debate = debates[0]
#   debate_links = debate.find('a')
#   if not debate_links:
#     continue
#   link = debate_links['href']
#   all_debates.append({'date':date,'debate':debate.text,'link':link})

transcript_files = []
for d in all_debates:
  http = urllib3.PoolManager()
  r = http.request('GET', d['link'])
  if r.status != 200:
    break
  file = bs4.BeautifulSoup(r.data)
  file_name = file.find_all('span',{'class':'paperstitle'})[0].text
  name_spl = file_name.split()
  spl = name_spl.index('in')
  place = "_".join(name_spl[spl:])
  name = os.path.join('debates',("_".join(name_spl) + ".html"))
  fo = open(name,"wb")
  fo.write(r.data)
  fo.close()
  time.sleep(5)

transcripts = []
moderators = []
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

for file in os.listdir('debates'):
  transcript_filename = os.path.join('debates',file)
  transcript = {"file":transcript_filename}
  with open(transcript_filename) as f:
    bsoup = bs4.BeautifulSoup(f)

  tran = bsoup.find_all('span',{'class':'displaytext'})
  
  date = bsoup.find_all('span',{'class':'docdate'})
  transcript['date'] = date[0].text
  date = date[0].text
  debate = file.strip(".html")
  party = debate.split("_")[0]
  loc = " ".join(debate.split("_")[2:])

  pars = tran[0].find_all('p')

  parsed = []

  for x in pars:
    t = re.sub('\[.*\]','',x.text) # line to cut out [applause] lines
    t = re.sub(ur'\u2014','-',t,re.UNICODE) #line to make em-dashes into single dashes
    t = re.sub(ur'\u00e1','a',t,re.UNICODE) #take out accented a
    t = re.sub(ur'\u00c1','a',t,re.UNICODE) #take out accented A
    mod = False
    if x.b:
      speaker = re.sub('\[.*\]','',x.b.text)
      speaker = re.sub(ur'\u00ed','i',speaker,re.UNICODE) #take out accented I #take out accented A
      speaker = re.sub(ur'\u00c1','A',speaker,re.UNICODE) #take out accented A

      tmp_speaker = str(speaker.encode('utf8').lower()).strip(":")
      if tmp_speaker not in candidates:
        mod = True
        if tmp_speaker not in moderators:
          moderators.append(tmp_speaker)
      elif tmp_speaker not in candidates and tmp_speaker not in moderators:
        candidates.append(tmp_speaker)
      parsed.append({'speaker':speaker.strip(":"),'speech':t, 'date':date, 'moderator':mod,'party':party,'location':loc})
    else:
      parsed[-1]['speech'] = parsed[-1]['speech'] + t

  transcript['tran'] = parsed
  transcripts.append(transcript)

with open('debate_data.json', 'w') as outfile:
    json.dump(transcripts, outfile, sort_keys=True, indent=4, separators=(',', ': '))

all_debate_list = []
for x in transcripts:
  all_debate_list = all_debate_list + x['tran']

with open('all_debate_list.json','w') as outfile:
  json.dump(all_debate_list, outfile, indent=4, separators=(',', ': '))
