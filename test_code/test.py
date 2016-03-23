import bs4
import re

transcript_filename = "miami_florida_dem.html"
with open(transcript_filename) as f:
    bsoup = bs4.BeautifulSoup(f)

tran = bsoup.find_all('span',{'class':'displaytext'})

pars = tran[0].find_all('p')

parsed = []

for x in pars:
  t = re.sub('\[.*\]','',x.text) # line to cut out [applause] lines
  #t = x.text
  if x.b:
    speaker = re.sub('\[.*\]','',x.b.text)
    parsed.append({'speaker':speaker.strip(":"),'speech':[t]})
  else:
    parsed[-1]['speech'].append(t)

for x in parsed[:20]:
  print(x)