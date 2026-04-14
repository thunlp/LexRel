import json
from time import sleep
import os
import re
import argparse
from vllm import LLM, SamplingParams

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7"
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True, help='')
args = parser.parse_args()

sampling_params = SamplingParams(temperature=0.7, max_tokens=8192)
llm = LLM(model=f"/path/to/{args.model}",tensor_parallel_size=8,dtype="bfloat16",gpu_memory_utilization=0.8,trust_remote_code=True) 

with open('/path/to/prompt.json', 'r', encoding='utf-8') as f:
    relation_prompt = json.load(f)

with open('/path/to/rdict.json', 'r', encoding='utf-8') as f:
    rdict = json.load(f)

with open(f'/path/to/output/{args.model}_type.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
with open(f'/path/to/output/{args.model}_argument.json', 'w',encoding='utf-8') as f1:
    f1.write('[\n')
    
    output = []
    batch_size = 16
    first_item = True

    for i in range(0, len(data), batch_size):
        batch_d = data[i:i+batch_size]
        batch = []
        batch_r = []
        
        for d in batch_d:
            subject = {}
            for r in d['predict_relation']:
                r = r.replace(' ','')
                try:
                    batch.append(relation_prompt[rdict[r]].format(r, d['input']))
                    batch_r.append(r)
                except:
                    continue

        try:
            outputs = llm.generate(batch, sampling_params)
            results = [output.outputs[0].text for output in outputs]  
            sleep(1)

            index = 0
            for j, d in enumerate(batch_d):
                subject = {}
                for k, r in enumerate(d['predict_relation']):
                    r = r.replace(' ','')
                    try:
                        matched_parts = re.findall(r'\{.*?\}', results[index])
                        subject[r] = list(set(matched_parts))
                        index += 1
                    except:
                        continue
                d['predict_subject'] = subject
                if not first_item:
                    f1.write(',\n')
                json.dump(d, f1, ensure_ascii=False)
                first_item = False
        except Exception as e:
            continue
    f1.write('\n]')