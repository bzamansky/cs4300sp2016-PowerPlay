import bs4, re, urllib3, time, os, json
import numpy as np
import matplotlib.pyplot as plt

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

topics = [
  'abortion',
  'immigration',
  'economy',
  'drugs',
  'guns',
  'environment',
  'education',
  'taxes',
  'marriage',
  'healthcare',
  'terrorism'
]

topics_occurence = [0] * len(topics) 

candidates_num_words = [0] * len(candidates)
candidates_num_speaches = [0] * len(candidates)

with open('all_debate_list.json') as data_file:
  documents = json.load(data_file)

topics_to_index = {}
for i,x in enumerate(topics):
  topics_to_index[x] = i
candidates_to_index = {}
for i,x in enumerate(candidates):
  candidates_to_index[x] = i

for item in documents:
  speaker = item['speaker'].lower()
  if speaker in candidates:
    candidates_num_speaches[candidates_to_index[speaker]] += 1
  for word in item['speech'].split(" "):
    if speaker in candidates:
      candidates_num_words[candidates_to_index[speaker]] += 1
    tmp = word.lower()
    if tmp in topics:
      topics_occurence[topics_to_index[tmp]] += 1

# N = len(topics)
# ind = np.arange(N)  # the x locations for the groups
# width = 0.7       # the width of the bars

# fig = plt.figure()
# ax = fig.add_subplot(111)
# rects1 = ax.bar(ind, topics_occurence, width, color='b')

# # add some text for labels, title and axes ticks
# ax.set_ylabel('Number of occurrences in debates')
# ax.set_title('Common topic words')
# ax.set_xticks(ind + width/2.)
# ax.set_xticklabels(topics)


# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                 '%d' % int(height),
#                 ha='center', va='bottom')

# autolabel(rects1)

# plt.show()

# N = len(candidates)
# ind = np.arange(N)  # the x locations for the groups
# width = 0.7       # the width of the bars

# fig = plt.figure()
# ax = fig.add_subplot(111)
# rects1 = ax.bar(ind, candidates_num_words, width, color='b')

# # add some text for labels, title and axes ticks
# ax.set_ylabel('Number of (total) words each candidates say')
# ax.set_title('Candidates')
# ax.set_xticks(ind + width/2.)
# ax.set_xticklabels(candidates)


# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                 '%d' % int(height),
#                 ha='center', va='bottom')

# autolabel(rects1)

#plt.show()

N = len(candidates)
ind = np.arange(N)  # the x locations for the groups
width = 0.7       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)
rects1 = ax.bar(ind, candidates_num_speaches, width, color='b')

# add some text for labels, title and axes ticks
ax.set_ylabel('Number of times each candidates speaks')
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

plt.show()
