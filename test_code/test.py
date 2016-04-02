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


# transcript_files = []
# for d in all_debates:
#   http = urllib3.PoolManager()
#   r = http.request('GET', d['link'])
#   if r.status != 200:
#     break
#   file = bs4.BeautifulSoup(r.data)
#   file_name = file.find_all('span',{'class':'paperstitle'})[0].text
#   name_spl = file_name.split()
#   name = os.path.join('debates',(name_spl[0] + "_" + name_spl[-2] + "_" + name_spl[-1] + ".html"))
#   fo = open(name,"wb")
#   fo.write(r.data)
#   fo.close()
#   time.sleep(5)


transcripts = []

for file in os.listdir('debates'):
  transcript_filename = os.path.join('debates',file)
  transcript = {"file":transcript_filename}
  with open(transcript_filename) as f:
    bsoup = bs4.BeautifulSoup(f)

  tran = bsoup.find_all('span',{'class':'displaytext'})

  pars = tran[0].find_all('p')

  parsed = []

  for x in pars:
    t = re.sub('\[.*\]','',x.text) # line to cut out [applause] lines
    t = re.sub(ur'\u2014','-',t,re.UNICODE)
    if x.b:
      speaker = re.sub('\[.*\]','',x.b.text)
      parsed.append({'speaker':speaker.strip(":"),'speech':[t]})
    else:
      parsed[-1]['speech'].append(t)

  transcript['tran'] = parsed
  transcripts.append(transcript)

with open('debate_data.json', 'w') as outfile:
    json.dump(transcripts, outfile, sort_keys=True, indent=4, separators=(',', ': '))
