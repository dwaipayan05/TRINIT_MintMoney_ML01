import json

f = open('COVID-QA_Clean.json')
data = json.load(f)
with open('COVID-QA_Clean.jsonl', 'w') as outfile:
    for entry in data:
        json.dump(entry, outfile)
f.close()