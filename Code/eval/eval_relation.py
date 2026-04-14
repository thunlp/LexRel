import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='deepseek-r1', help='要使用的模型名称')
args = parser.parse_args()

if __name__ == "__main__":
    with open(f'/path/to/data/{args.model}_type.json', 'r', encoding='utf-8') as f:
        pred_json = json.load(f)
    
    total_tp = 0
    total_fp = 0
    total_fn = 0
    
    for p in pred_json:
        try:
            pred_set = set(p['predict_relation'])
            true_set_for_item = set(p['relation'].keys())
            
            tp = len(pred_set & true_set_for_item)
            fp = len(pred_set - true_set_for_item)
            fn = len(true_set_for_item - pred_set)
            
            total_tp += tp
            total_fp += fp
            total_fn += fn
            
        except KeyError:
            continue
        
    precision = total_tp / (total_tp + total_fp) if (total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}")