from vllm import LLM, SamplingParams
import json
from tqdm import tqdm
import glob
import os
from time import sleep
import re
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=False,default="Qwen3-32B", help='要使用的模型名称')
args = parser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7"

with open('/path/to/prompt.json', 'r', encoding='utf-8') as f:
    realtion_prompt = json.load(f)
with open('/path/to/rdict.json', 'r', encoding='utf-8') as f:
    rdict = json.load(f)

data = []
json_files = glob.glob('/path/to/test.json')
for file in tqdm(json_files):
    with open(file, 'r', encoding='utf-8') as f:
        data.extend(json.load(f))

sampling_params = SamplingParams(temperature=0.7, max_tokens=8192)
llm = LLM(model=f"/path/to/{args.model}",tensor_parallel_size=8,dtype="bfloat16",gpu_memory_utilization=0.8,trust_remote_code=True)

output = []
with open(f'/path/to/output/{args.model}_type.json', 'w', encoding='utf-8') as f:
    f.write('[\n')
    
    first_item = True
    batch_size = 16
    r_set = set(rdict.keys())
    index = 0
    batch = []
    for d in data:
        if d['input'] !='':
            batch.append(d)
            if batch_size == len(batch) or d == data[-1]:
                inputs = []
                for d in batch:
                    prompt = realtion_prompt['WZ'].format(d['input'],str(rdict.keys()))
                    inputs.append(prompt)
                
                outputs = llm.generate(inputs, sampling_params)
                results = [output.outputs[0].text for output in outputs]  
                sleep(1)
                for i,r in zip(batch,results):
                    try:
                        r_list = re.findall(r'\[(.*?)\]',r)[-1].replace("，",",").replace("'",'').replace(" ",'').split(',')
                    except Exception as e:
                        r_list = []
                    print(r_list)
                    r_list = [item for item in r_list if item in r_set]
                    i["predict_relation"] = r_list
                
                    if not first_item:
                        f.write(',\n')
                    json.dump(i, f, ensure_ascii=False)
                    index += 1
                    first_item = False
                batch = []
    
    f.write('\n]')