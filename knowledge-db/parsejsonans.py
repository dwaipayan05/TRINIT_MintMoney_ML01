import json

f = open('COVID-QA.json')
data = json.load(f)

document_id = 1
data_dict = []


count = 0
for paragraph in data['data']:
    for context in paragraph['paragraphs']:
        for qs in context['qas']:
            for ans in qs['answers']:
                j = {
             "prompt" : qs['question'],
             "completion" : ans['text']
            }

            data_dict.append(j)

json_dump = json.dumps(data_dict, indent = 3)
with open("COVID-QAOnly_clean.json","w") as outfile:
    outfile.write(json_dump)


x = open('COVID-QAOnly_Clean.json')
data = json.load(x)
with open('COVID-QAOnly_Clean.jsonl', 'w') as outfile:
    for entry in data:
        json.dump(entry, outfile)
        outfile.write('\n')
x.close()

f.close()
