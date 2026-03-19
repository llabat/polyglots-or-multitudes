# Polyglots or Multitudes? Multilingual LLM Answers to Value-laden Multiple-Choice Questions

This repository contains the code and data used in the paper:

> [Polyglots or Multitudes? Multilingual LLM Answers to Value-laden Multiple-Choice Questions](https://arxiv.org/abs/2602.05932) (EACL 2026, main conference)

---

## Repository Structure

```
.
├── exp_config.yaml      # Experiment configuration
├── launcher.py          # Experiment launcher (multi-model runs)
├── mcp.py               # Multiple-choice prompting functions
├── run.py               # Main script for administering MCQs
├── utils.py             # Model loading + utilities
├── mevs/
│   ├── data/
│   │   ├── MEVS.json    # Core dataset
    │   ├── ...
│   └── mevs/
│       ├── generator.py # Prompt generation
│       ├── const.py     # Symbols, mappings
│       ├── ...
```

---

## Dataset: MEVS

The **Multilingual European Value Survey (MEVS)** is a curated dataset of:

- 8 European languages  
- 142 questions related to **values**
- Human-translated 


---

## Getting Started

### 1. Install dependencies

```
pip install -r requirements.txt
```

---

### 2. Run an experiment

```
python run.py --config exp_config.yaml
```

Or via launcher:

```
python launcher.py exp_config.yaml
```

---

## ⚙️ Configuration

All experiments are controlled via:

```yaml
dataset:
  path: mevs/data/MEVS.json

  dataset:
  path: mevs/data/MEVS.json
  question_set: [13, 14, 15, 16, 17, 40, 41, 42, 43, 44]
  languages: ["FRE_FR", "SPA_ES", "ENG_GB"]

prompt:
  symbols: ["letters", "numbers"]
  tail: ["none", "space", "newline"]
  order: ["all"]

models:
  - QuixiAI/Wizard-Vicuna-7B-Uncensored
  - Qwen/Qwen2.5-7B-Instruct

precision: 32
output_dir: results/
```

### 1. Model ('models')

A *list* of models to administer the questionnaire to. This parameter is overriden when using run.py.

Additional model-related optional parameters include:
- *precision*: a precision parameter for the version of the model to load (8, 16 or 32). We used 32 when possible, 16 otherwise.
- *model_cache*: a path if models are stored in a custom cache (as is the case in our HPC)


### 2. Language ('languages')
A *list* of language-country codes. Supported languages include :
- English (**"ENG_GB"**)
- Spanish (**"SPA_ES"**)
- French (**"FRE_FR"**)
- German (**"GER_DE"**)
- Czech (**"CZE_CZ"**)
- Russian (**"RUS_RU"**)
- Norwegian (**"NOR_NO"**)

### 3. Symbol type ('symbols')
A *list* of symbol types ("letters", "numbers").

### 4. Tail characters ('tail')
A *list* of tail characters ("none", "space", "newline").

### 5. Answer order ('order')

A *list* of order types to test. Three types of arguments are supported:

- "default" (the order of the successor function)
- "random" (a **single** random order)
- "all" (n! orders for a question with n options)

In our experiments, we used 'all' to test the orders **comprehensively**.

---

## 🧪 Methodology

For each question:

1. Generate all prompt variants  
2. Pass the prompts to the LLM
3. Extract the answer token with highest log-probability


---


## 📚 Citation

```bibtex
@article{labat2026polyglots,
  title={Polyglots or Multitudes? Multilingual LLM Answers to Value-laden Multiple-Choice Questions},
  author={Labat, Léo and Ollion, Etienne and Yvon, François},
  year={2026},
  journal={EACL}
}
```

---

## 📜 License

*(TODO — you need to decide this explicitly)*

Recommendation:
- Code → MIT  
- Data → CC-BY-NC  

---

## Notes

- This repo focuses on **MCQ-based evaluation**, not generation  
- Requires access to models exposing **token probabilities**  
- Designed for **controlled experimental reproducibility**

---
