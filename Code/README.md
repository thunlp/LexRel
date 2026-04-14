# LegalRel: Code

This repository contains the data construction and evaluation code for LegalRelBench, a benchmark for legal relation extraction tasks.

---

## 📁 Project Structure

### 1. `train/` - Training Configuration

Contains configuration files for the [LlamaFactory](https://github.com/hiyouga/LLaMA-Factory) training framework, used for model fine-tuning.

### 2. `generate/` - Data Generation

Code for generating legal relation data:

| File                                                                | Description                                                                                        |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `generate_type_vllm.py` / `generate_type_api.py`                | Legal relation type generation (supporting vLLM and API inference respectively)                    |
| `generate_argument_vllm.py` / `generate_argument_api.py`        | Legal relation argument generation (supporting vLLM and API inference respectively)                |
| `generate_lawbench_type.py `  / `generate_lawbench_argument.py` | Generate legal relation types and arguments for [Lawbench](https://github.com/open-compass/LawBench) |

### 3. `eval/` - Evaluation Scripts

Contains two evaluation scripts for:

- Evaluating legal relation type predictions
- Evaluating legal relation argument predictions
