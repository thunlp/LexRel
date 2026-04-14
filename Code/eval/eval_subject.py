import json
from Code.load_model import batch_llm_response
import asyncio
import os
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=False,default="deepseek-v3-250324", help='要使用的模型名称')
args = parser.parse_args()

if __name__ == "__main__":
    with open(f'/path/to/{args.model}_argument.json', 'r', encoding='utf-8') as f:
        pred_json = json.load(f)
    
    total_correct = 0  
    total_predicted = 0 
    total_true = 0  
    all_results = []  
    
    evaluation_prompts = []
    for p in tqdm(pred_json):
        pred_set = p['predict_subject']
        true_set = p['label']
        for k1,v1 in true_set.items():
            if k1 not in pred_set:
                total_true += len(v1)
        for k,v in pred_set.items():
            if k not in true_set:
                total_predicted += len(v)
            else:
                prompt = f"""请分别对 AI 回答的准确率和召回率进行评分，定义如下：
                    • 准确率= 模型回答中正确条目数 ÷ 回答的总条目数
                    • 召回率 = 模型回答中正确条目数 ÷ 标准答案的总条目数

                    AI 回答的预测结果和真实结果都是多个列表的形式，每个列表就是一个条目。请按照以下规则计算正确条目数：
                    1. 顺序不重要，只要条目中主要信息正确即视为正确
                    2. 重复条目不重复计数
                    
                    AI 回答的预测结果和真实结果如下:
                    - 预测结果: {str(v)}
                    - 真实结果: {str(true_set[k])}
                    
                    请按照以下格式返回结果:
                    {{
                        "precision": {{
                            "correct": <正确条目数>,
                            "total": <预测总条目数>,
                            "score": <准确率评分>
                        }},
                        "recall": {{
                            "correct": <正确条目数>,
                            "total": <真实总条目数>,
                            "score": <召回率评分>
                        }}
                    }}"""
                evaluation_prompts.append(prompt)
            if len(evaluation_prompts) >= 16 or p==pred_json[-1]:
                evaluation_results = asyncio.run(batch_llm_response(evaluation_prompts, model="deepseek-v3-250324"))
                evaluation_prompts = []
        
                for i, result in enumerate(evaluation_results):
                    try:
                        import re
                        result = result.strip().replace('\n', '').replace('json', '')
                        json_match = re.findall(r'```(.*?)```', result)
                        if json_match:
                            eval_data = json.loads(json_match[-1])
                        else:
                            eval_data = json.loads(result)
                        
                        # 累加统计值
                        total_correct += eval_data['precision']['correct']
                        total_predicted += eval_data['precision']['total']
                        total_true += eval_data['recall']['total']
                        
                        sample_result = {
                            'prediction': pred_json[i]['predict_subject'],
                            'label': pred_json[i]['relation'],
                            'precision': eval_data['precision'],
                            'recall': eval_data['recall']
                        }
                        all_results.append(sample_result)
                        
                    except Exception as e:
                        print(f"样本 {i} 评估结果解析失败: {result}")

    total_precision = total_correct / total_predicted if total_predicted > 0 else 0
    total_recall = total_correct / total_true if total_true > 0 else 0
    
    output_dir = '/path/to/eval_result'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/{args.model}_evaluation_details.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    summary = {
        'total_precision': total_precision,
        'total_recall': total_recall,
        'total_correct': total_correct,
        'total_predicted': total_predicted,
        'total_true': total_true,
        'total_samples': len(all_results)
    }
    
    with open(f'{output_dir}/{args.model}_evaluation_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("\n最终统计结果:")
    print(f"总正确数: {summary['total_correct']}")
    print(f"预测总条目数: {summary['total_predicted']}")
    print(f"真实总条目数: {summary['total_true']}")
    print(f"总准确率: {summary['total_precision']:.4f}")
    print(f"总召回率: {summary['total_recall']:.4f}")
    print(f"F1: {2 * (summary['total_precision'] * summary['total_recall']) / (summary['total_precision'] + summary['total_recall']):.4f}")
    print(f"总样本数: {summary['total_samples']}")