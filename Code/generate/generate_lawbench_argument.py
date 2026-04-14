import json
from tqdm import tqdm
from Code.load_model import batch_llm_response
import asyncio
import os
import glob
    
with open('/path/to/Prompts/relation_prompt_v4.json', 'r', encoding='utf-8') as f:
    relation_prompt = json.load(f)
with open('/path/to/Prompts/rdict_v3.json', 'r', encoding='utf-8') as f:
    rdict = json.load(f)

input_folder = "/path/to/input"
output_folder = "/path/to/output"
os.makedirs(output_folder, exist_ok=True)

json_files = glob.glob(os.path.join(input_folder, "*.json"))

for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    output_file = os.path.join(output_folder, os.path.basename(json_file))
    
    with open(output_file, 'w', encoding='utf-8') as f1:
        f1.write('[\n')
        output = []
        batch_size = 16
        first_item = True
        for i in tqdm(range(0, len(data), batch_size)):
            batch_d = data[i:i+batch_size]
            batch = []
            batch_r = []
            
            for d in batch_d:
                subject = {}
                for r in d['relation']:
                    r = r.replace(' ','').replace('"','')
                    try:
                        batch.append(relation_prompt[rdict[r]].format(r, f"{d['instruction']}\n{d['question']}".replace("判决文书","陈述")+"\n5. 如果没有主体、客体和内容，可以不输出。"))
                    except:
                        continue
            try:
                results = asyncio.run(batch_llm_response(batch,"deepseek-v3-250324"))
                index = 0
                for j, i in enumerate(batch_d):
                    subject = {}
                    for k, r in enumerate(i['relation']):
                        r = r.replace(' ','')
                        try:
                            subject[r] = results[index]
                            index += 1
                        except:
                            continue
                    i['subject'] = subject
                    if not first_item:
                        f1.write(',\n')
                    json.dump(i, f1, ensure_ascii=False)
                    first_item = False
            except Exception as e:
                continue
        f1.write('\n]')