import json

with open("debate_data.json", "r") as f:
	debates = json.load(f)

# get number of debates each candidate participated in
cand_dict = {
	'clinton': 0,
	'sanders': 0,
	"o'malley": 0,
	'chafee': 0,
	'webb': 0,
	'cruz': 0,
	'kasich': 0,
	'trump': 0,
	'rubio': 0,
	'carson': 0,
	'bush': 0,
	'christie': 0,
	'fiorina': 0,
	'santorum': 0,
	'paul': 0,
	'huckabee': 0,
	'pataki': 0,
	'graham': 0,
	'jindal': 0,
	'walker': 0,
	'perry': 0
}

for d in debates:
	for line in d['tran']:
		speaker = str(line['speaker'])
		speaks = 0
		if (speaker in cand_dict.keys()):
			speaks = 1
	if (speaker in cand_dict.keys()):
		cand_dict[speaker] += speaks

print(cand_dict)