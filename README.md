# 🎭 Polyglots or Multitudes? Multilingual LLM Answers to Value-laden Multiple-Choice Questions

This repository contains the code and data used in the paper:

> [Polyglots or Multitudes? Multilingual LLM Answers to Value-laden Multiple-Choice Questions](https://arxiv.org/abs/2602.05932) (EACL 2026, main conference)

---

## 📁 Repository Structure

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

## 📖 The MEVS Dataset

The **Multilingual European Value Survey (MEVS)** is a curated dataset of:

- 142 questions related to **values**
- Human-translated 
- in 8 European languages  



---

## ♻️ Reproducing the results

### 1. Install dependencies

```
pip install -r requirements.txt
```

---

### 2. Adjust the configuration file

Define a list of models, questions, languages and other formatting variables and adjust infrastructure-dependent paths in the configuration file (cf. the **Configuration** section below).


### 3. Run the experiments

Run an experiment on a single model:

```
python run.py --config exp_config.yaml --model model_name
```

Or administer MEVS questions to several models using the launcher:

```
python launcher.py exp_config.yaml
```

---

## ⚙️ Configuration

All experiments are controlled via a yaml config file such as:

```yaml
dataset:
  path: mevs/data/MEVS.json
  question_set: [13, 14, 15, 16, 17, 40, 41, 42, 43, 44]
  languages: ["FRE_FR", "SPA_ES", "ENG_GB"]

prompt:
  symbols: ["letters", "numbers"]
  tail: ["none", "space", "newline"]
  order: ["all"]

models:
  - meta-llama/Llama-3.1-8B-Instruct
  - Qwen/Qwen2.5-7B-Instruct
precision: 32

output_dir: results/
```
### Questions ('dataset' > 'question_set')

A list of question identifiers referring to MEVS questions. The development set of the paper is made up of 10 questions: [13, 14, 15, 16, 17, 40, 41, 42, 43, 44].

The IDs of the 24 questions used for the most consistent models are: [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 86, 87, 88, 89, 118, 119, 120, 121, 122, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138].

### Model ('models')

A *list* of models to administer the questionnaire to. This parameter is overriden when using run.py.

Additional model-related optional parameters include:
- *precision*: a precision parameter for the version of the model to load (8, 16 or 32). We used 32 when possible, 16 otherwise.
- *model_cache*: a path if models are stored in a custom cache (as is the case in our HPC)

### Language ('dataset' > 'languages')
A *list* of language-country codes. Supported languages include :
- English (**"ENG_GB"**)
- Spanish (**"SPA_ES"**)
- French (**"FRE_FR"**)
- German (**"GER_DE"**)
- Czech (**"CZE_CZ"**)
- Russian (**"RUS_RU"**)
- Norwegian (**"NOR_NO"**)

### Symbol type ('prompt' > 'symbols')
A *list* of symbol types ("letters", "numbers").

### Tail characters ('prompt' > 'tail')
A *list* of tail characters ("none", "space", "newline").

### Answer order ('prompt' > 'order')

A *list* of order types to test. Three types of arguments are supported:

- "default" (the order of the successor function)
- "random" (a **single** random order)
- "all" (n! orders for a question with n options)

In our experiments, we used 'all' to test the orders **comprehensively**.

### Output directory ('output_dir')

A string denoting a path to a directory in which results will be saved batch by batch. If the directory does not exist, it will be created. Make sure you keep results from previous runs in that location to avoid rerunning prompts you have already processed.

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
