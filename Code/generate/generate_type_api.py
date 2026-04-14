import json
from time import sleep
from Code.load_model import batch_llm_response
import asyncio

with open('/path/to/Prompts/legal_relation_prompt.json', 'r', encoding='utf-8') as f:
    relation_prompt = json.load(f)
with open('/path/to/Prompts/legal_relation_dict.json', 'r', encoding='utf-8') as f:
    rdict = json.load(f)

data = []
with open("/path/to/data/test_original.json", 'r', encoding='utf-8') as f:
    data.extend(json.load(f))

    
output = []
with open('/path/to/data/test_draft_type.json', 'w', encoding='utf-8') as f:
    f.write('[\n')
    
    first_item = True
    batch_size = 16
    r_set = set(rdict.keys())
    index = 0
    batch = []
    
    for d in data:
        if d['SS'] !='':
            batch.append(d)
            if batch_size == len(batch):
                print(f"正在处理批次{index}-{index+batch_size}...")
                inputs = []
                for d in batch:
                    prompt = relation_prompt['WZ'].format(d['QW'],str(rdict.keys()))
                    inputs.append(prompt)
                results = asyncio.run(batch_llm_response(inputs,"model"))
                sleep(3)
                print(results)
                for i,r in zip(batch,results):
                    r = r.split('</think>')[-1].replace(' ','').strip() 
                    r = r.replace('，',',').replace("[","").replace("]","").replace("'","").replace('"',"")
                    r_list = r.split(',')
                    r_list = [item for item in r_list if item in r_set]
                    if r_list != []:
                        item = {"uniqid":i['uniqid'],"SS":i['SS'],"QW":i['QW'],"All":r_list}
                    
                        if not first_item:
                            f.write(',\n')
                        json.dump(item, f, ensure_ascii=False)
                        index += 1
                        first_item = False
                batch = []
    inputs = []
    for d in batch:
        prompt = relation_prompt['WZ'].format(d['QW'],str(rdict.keys()))
        inputs.append(prompt)
    results = asyncio.run(batch_llm_response(inputs))
    sleep(3)
    for i,r in zip(batch,results):
        r = r.split('</think>')[-1].replace(' ','').strip() 
        r = r.replace('，',',').replace("[","").replace("]","").replace("'","").replace('"',"")
        r_list = r.split(',')
        r_list = [item for item in r_list if item in r_set]
        if r_list != []:
            item = {"uniqid":i['uniqid'],"SS":i['SS'],"QW":i['QW'],"All":r_list}
                    
            if not first_item:
                f.write(',\n')
            json.dump(item, f, ensure_ascii=False)
            index += 1
            first_item = False
    batch = []
    f.write('\n]')