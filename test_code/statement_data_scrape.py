import bs4, re, urllib3, time, os, json

campaign_speeches = [
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=70&campaign=2016CLINTON&doctype=5000",
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=107&campaign=2016SANDERS&doctype=5000",
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=103&campaign=2016CRUZ&doctype=5000",
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=114&campaign=2016KASICH&doctype=5000",
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=115&campaign=2016TRUMP&doctype=5000" 
]
campaign_speech_pages = []

statements = [
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=107&campaign=2016SANDERS&doctype=5001",
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=103&campaign=2016CRUZ&doctype=5001",
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=114&campaign=2016KASICH&doctype=5001",
  "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=115&campaign=2016TRUMP&doctype=5001"  
]

statement_pages = []

transcript_files = []
for d in campaign_speeches:
  http = urllib3.PoolManager()
  r = http.request('GET', d)
  if r.status != 200:
    break
  file = bs4.BeautifulSoup(r.data)
  file_table = file.find_all("td",{'class':"listdate"})
  candidate = file_table[0].text.split(" ")[1].lower()
  speech_tags = [(x.find_all("a")[0].text,x.find_all("a")[0]['href']) for x in file_table if len(x.find_all("a")) > 0]
  speech_tags = [x for x in speech_tags if x[0].split(" ")[0] == "Remarks" or x[0].split(" ")[0] == "Interview"]
  speech_links = [x[1].strip("..") for x in speech_tags]
  speech_links = [("http://www.presidency.ucsb.edu" + x, candidate) for x in speech_links]
  campaign_speech_pages.extend(speech_links)

candidate_data = {}

for x in campaign_speech_pages:
  candidate_data[x[1]] = []


for d in campaign_speech_pages:
  candidate = d[1]
  http = urllib3.PoolManager()
  r = http.request('GET', d[0])
  if r.status != 200:
    break
  file = bs4.BeautifulSoup(r.data)
  date = file.find_all('span',{'class':'docdate'})[0].text
  title = file.find_all('span',{'class':'paperstitle'})[0].text
  text = file.find_all("span",{"class":"displaytext"})[0]


  all_lines = text.contents
  all_lines[:2] = []
  for line in all_lines: 
    if type(line) is bs4.element.NavigableString:
      continue
    if line.b:
      speaker = re.sub('\[.*\]','',line.b.text)
    elif line.i:
      speaker = re.sub('\[.*\]','',line.i.text)
    speaker = speaker.lower()
    speaker = speaker.strip(":")
    try:
      line.text
    except Exception, e:
      line = re.sub('\[.*\]','',line)
    else:
      line = re.sub('\[.*\]','',line.text)     
    if speaker in candidate_data:
      line = line.replace(speaker.title() + ": ","")
      line = line.replace(speaker.title() + ":","")
      line = line.replace(speaker.upper() + ": ", "")
      line = line.replace(speaker.upper() + ":", "")
      candidate_data[speaker].append(line)


for d in statements:
  http = urllib3.PoolManager()
  r = http.request('GET', d)
  if r.status != 200:
    break
  file = bs4.BeautifulSoup(r.data)
  file_table = file.find_all("td",{'class':"listdate"})
  candidate = file_table[0].text.split(" ")[1].lower()
  speech_links = [x.find_all("a")[0]['href'] for x in file_table if len(x.find_all("a")) > 0]
  speech_links = [x.strip("..") for x in speech_links]
  speech_links = [("http://www.presidency.ucsb.edu" + x, candidate) for x in speech_links]
  statement_pages.extend(speech_links)

for d in statement_pages:
  candidate = d[1]
  http = urllib3.PoolManager()
  r = http.request('GET', d[0])
  if r.status != 200:
    break
  file = bs4.BeautifulSoup(r.data)
  date = file.find_all('span',{'class':'docdate'})[0].text
  title = file.find_all('span',{'class':'paperstitle'})[0].text
  text = file.find_all("span",{"class":"displaytext"})[0]

  all_lines = text.contents
  all_lines[:2] = []
  for i,line in enumerate(all_lines):   
    try:
      line.text
    except Exception, e:
      line = re.sub('\[.*\]','',line)
    else:
      line = re.sub('\[.*\]','',line.text)
    candidate_data[candidate].append(line)

with open('candidate_statements.json','w') as outfile:
  json.dump(candidate_data, outfile, sort_keys=True, indent=4,separators=(',', ': '))