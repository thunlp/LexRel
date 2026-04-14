import json
from tqdm import tqdm
from Code.load_model import batch_llm_response
import asyncio
import os
import glob

with open('/path/to/Prompts/legal_relation_prompt.json', 'r', encoding='utf-8') as f:
    relation_prompt = json.load(f)
with open('/path/to/Prompts/legal_relation_dict.json', 'r', encoding='utf-8') as f:
    rdict = json.load(f)

input_folder = "/path/to/input"
output_folder = "/path/to/output"
os.makedirs(output_folder, exist_ok=True)

json_files = glob.glob(os.path.join(input_folder, "*.json"))
for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output_file = os.path.join(output_folder, os.path.basename(json_file))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('[\n') 
        
        first_item = True
        batch_size = 16
        r_set = set(rdict.keys())
        index = 0
        batch = []
        
        for d in tqdm(data):
            batch.append(d)
            if batch_size == len(batch) or d == data[-1]:
                print(f"正在处理文件 {os.path.basename(json_file)} 的批次 {index}-{index+len(batch)}...")
                inputs = []
                for d in batch:
                    prompt = relation_prompt['WZ'].format(f"{d['instruction']}\n{d['question']}", str(rdict.keys())) \
                            .replace("判决书文本", "陈述") \
                            .replace('判决书内容', '陈述内容')
                    inputs.append(prompt)
                
                results = asyncio.run(batch_llm_response(inputs, 'deepseek-v3-250324'))
                
                for i, r in zip(batch, results):
                    r = r.replace(' ', '').strip()
                    r = r.replace('，', ',').replace("[", "").replace("]", "").replace("'", "").replace('"', "")
                    r_list = r.split(',')
                    r_list = [item for item in r_list if item in r_set]
                    relation = []
                    if len(r_list) != 0:
                        for r in r_list:
                            if r in rdict.keys():
                                relation.append(r)
                    i['relation'] = relation
                    if not first_item:
                        f.write(',\n')
                    json.dump(i, f, ensure_ascii=False)
                    index += 1
                    first_item = False
                
                batch = []
        
        f.write('\n]')