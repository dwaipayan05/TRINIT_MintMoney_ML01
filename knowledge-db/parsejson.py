import json

f = open('COVID-QA.json')
data = json.load(f)

document_id = 1
data_dict = []


for paragraph in data['data']:
    for context in paragraph['paragraphs']:
         j = {
             "text" : context['context'],
             "metadata" : document_id
         }

         document_id = document_id + 1
         data_dict.append(j)

json_dump = json.dumps(data_dict, indent = 3)
with open("COVID-QA_clean.json","w") as outfile:
    outfile.write(json_dump)

f.close()