import json
from time import sleep
from Code.load_model import batch_llm_response_sub
import asyncio
    
with open('/path/to/Prompts/legal_relation_prompt.json', 'r', encoding='utf-8') as f:
    realtion_prompt = json.load(f)
with open('/path/to/data/test_draft_type.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('/path/to/Prompts/legal_relation_dict.json', 'r', encoding='utf-8') as f:
    rdict = json.load(f)
with open('/path/to/data/test_draft.json', 'w',encoding='utf-8') as f1:
    f1.write('[\n')
    
    output = []
    batch_size = 16
    first_item = True
    print(len(data))
    for i in range(0, len(data), batch_size):
        batch_d = data[i:i+batch_size]
        batch = []
        batch_r = []
        
        for d in batch_d:
            subject = {}
            for r in d['All']:
                r = r.replace(' ','')
                try:
                    batch.append(realtion_prompt[rdict[r]].format(r, d['QW']))
                    batch_r.append(r)
                except:
                    continue
        
        try:
            results = asyncio.run(batch_llm_response_sub(batch,"model"))
            sleep(1)
            print(results)
            index = 0
            for j, d in enumerate(batch_d):
                subject = {}
                for k, r in enumerate(d['All']):
                    r = r.replace(' ','')
                    try:
                        subject[r] = results[index]  # 分配结果
                        index += 1
                    except:
                        continue
                item = {
                    "uniqid": d['uniqid'],
                    "SS": d['SS'],
                    "QW": d['QW'],
                    "All": d['All'],
                    "subject-object": subject
                }
                if not first_item:
                    f1.write(',\n')
                json.dump(item, f1, ensure_ascii=False)
                first_item = False
        except Exception as e:
            continue
    f1.write('\n]')