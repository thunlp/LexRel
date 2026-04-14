<h1 align="center">LexRel: Legal Relation Extraction Benchmark<br>for Chinese Civil Cases</h1>

# News

- 🚀 [2026/04/14]: We release the **LexRel** dataset, along with the complete pipeline for data generation, training, and evaluation!
- 🎉 [2026/04/05]: Our paper has been accepted to the **ACL 2026** Main Conference!
- 📄 [2025/12/14]: Our preprint [LexRel: Benchmarking Legal Relation Extraction for Chinese Civil Cases](https://arxiv.org/abs/2512.12643) is now available on arXiv!

# Links

- 📜 [Paper](https://arxiv.org/abs/2512.12643)
- 🌍 [Github](https://github.com/thunlp/LexRel)

# Introduction

Legal relations form a highly consequential analytical framework of civil law system, serving as a crucial foundation for resolving disputes and realizing values of the rule of law in judicial practice. However, legal relations in Chinese civil cases remain underexplored in the field of legal artificial intelligence (legal AI), largely due to the absence of comprehensive schemas.

In this work, we firstly introduce a comprehensive schema, which contains a hierarchical taxonomy and definitions of arguments, for AI systems to capture legal relations in Chinese civil cases. Based on this schema, we then formulate legal relation extraction task and present **LexRel**, an expert-annotated benchmark for legal relation extraction in Chinese civil law. We use **LexRel** to evaluate state-of-the-art large language models (LLMs) on legal relation extractions, showing that current LLMs exhibit significant limitations in accurately identifying civil legal relations. Furthermore, we demonstrate that incorporating legal relations information leads to promising performance gains on other downstream legal AI tasks.

# Project Structure

The repository is organized into the following folders:

| Folder        | Description                                                                                                                            |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------- |
| `Taxonomy/` | Contains the comprehensive hierarchical taxonomy of legal relations in Chinese civil law, available in both Chinese and English (PDF). |
| `LexRel/`   | Contains the LexRel dataset files (`train_r1.json`, `train_4o.json`, and `test.json`) in JSON format.                            |
| `Code/`     | Contains the complete pipeline for the project, including data generation, model training, and evaluation scripts.                     |
| `Prompts/`  | Contains the prompt templates used for legal relation extraction and the definition dictionary for all legal relations.                |

# Dataset Statistics

| Split           |          Samples |
| :-------------- | ---------------: |
| Train (R1)      |           19,798 |
| Train (4o)      |           17,706 |
| Test            |            1,140 |
| **Total** | **38,644** |

The dataset covers **106 unique legal relation types** in Chinese civil law.
Here are the top 10 most frequent relation types:

| Relation Type                  | Translation                                                          | Count |
| :----------------------------- | :------------------------------------------------------------------- | ----: |
| 借款合同关系                   | Legal Relation Arising from a Loan Contract                          |   536 |
| 保证合同关系                   | Legal Relation Arising from a Guarantee Contract                     |   223 |
| 夫妻关系                       | Conjugal Relationship                                                |   122 |
| 机动车交通事故侵权责任法律关系 | Legal Relation of Motor Vehicle Accident Tort Liability              |   104 |
| 财产保险合同关系               | Legal Relation Arising from a Property Insurance Contract            |   103 |
| 除房屋外的买卖合同关系         | Legal Relation Arising from a Sales Contract (excluding real estate) |    94 |
| 抵押合同关系                   | Legal Relation Arising from a Mortgage Contract                      |    63 |
| 房屋买卖合同关系               | Legal Relation Arising from a Real Estate Sales Contract             |    49 |
| 追偿权关系                     | Legal Relation of Right of Recourse                                  |    49 |
| 劳务合同关系                   | Legal Relation Arising from a Labor Service Contract                 |    41 |

# Dataset Format

Each sample in the dataset follows this JSON structure:

```json
{
    "uniqid": "unique-identifier-uuid",
    "input": "Fact descriptions extracted from the case...",
    "relation": {
        "Relation Type 1": [
            {
                "主体": "Party A, Party B",
                "客体": "The object of the legal relation",
                "内容": "Rights: ...\n\nObligations: ..."
            }
        ],
        "Relation Type 2": [
            {
                "主体": "Party A, Party B, Party C",
                "客体": "The object of the legal relation",
                "内容": "Rights: ...\n\nObligations: ..."
            }
        ]
    }
}
```

### Field Descriptions

| Field              | Description                                                                             |
| :----------------- | :-------------------------------------------------------------------------------------- |
| `uniqid`         | Unique identifier for each sample (UUID format)                                         |
| `input`          | Fact descriptions extracted from the civil case, typically numbered as factual findings |
| `relation`       | A dictionary mapping relation types to their argument details                           |
| `主体` (Subject) | The parties initiating or holding the right or obligation in the legal relation         |
| `客体` (Object)  | The counterparty or legal target of the legal relation                                 |
| `内容` (Content) | The rights and obligations associated with the legal relation                           |

# Dataset Example

```json
{
    "uniqid": "04305d7c-72cb-499d-b93c-8764def8ffd0",
    "input": "1. 2015年9月20日经派出所调解，被告高于贺承诺不再利用QQ、微信、支付宝等网络对外传播关于原告牛梦瑶的不良信息；\n2. 2016年3月30日，被告高于贺将原告牛梦瑶的裸照通过QQ、微信群发布；\n3. 原告牛梦瑶为诉讼花费律师费3000元；\n4. 被告高于贺因侵权行为已接受公安机关作出拘留10日的行政处罚；\n5. 被告高于贺利用QQ、微信等信息网络工具，在未经原告牛梦瑶允许的情况下，私自发布、散播原告牛梦瑶隐私照片。",
    "relation": {
        "隐私权侵权责任法律关系": [
            {
                "主体": "高于贺，牛梦瑶",
                "客体": "隐私权",
                "内容": "权利： 权利人有权请求侵权人停止侵害、赔偿精神损害抚慰金等民事责任。\n\n义务： 侵权人不得非法传播、散布他人隐私信息。\n"
            }
        ]
    }
}
```

## License

This dataset is released for research purposes only. Please refer to the paper for detailed license information.

## Citation

```bibtex
@misc{cai2025lexrelbenchmarkinglegalrelation,
      title={LexRel: Benchmarking Legal Relation Extraction for Chinese Civil Cases}, 
      author={Yida Cai and Ranjuexiao Hu and Huiyuan Xie and Chenyang Li and Yun Liu and Yuxiao Ye and Zhenghao Liu and Weixing Shen and Zhiyuan Liu},
      year={2025},
      eprint={2512.12643},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2512.12643}, 
}
```
