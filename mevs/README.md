# The Multilingual European Value Survey (MEVS)

This repository provides the **MEVS corpus** used in the paper [Polyglots or Multitudes? Multilingual LLM Answers to Value-laden Multiple-Choice Questions](https://arxiv.org/abs/2602.05932) by
Léo Labat, Etienne Ollion, François Yvon (EACL 2026)

It contains files and utilities needed to generate the prompts used in the experiments but also to reuse the corpus for other purposes.

------------------------------------------------------------------------

# Contents

The dataset includes:

    data/
    ├── MEVS.json
    ├── mevs_parallel_corpus.csv
    └── mevs_prompts_default.csv

## MEVS.json

This file contains the abstract structure of all MEVS questions as well as translations of all survey items in 8 European languages. Each question is a python dictionary containing a list of request ids and a list of response ids. To generate a question in a particular language, a dictionary of dictionaries ("translations") allows for the retrieval of actual natural language strings.

``` python
# Structure of MEVS.json

{"questionnaire_name": "multilingual_evs", 

# Dictionary of questions
 "questions": 
    {"0": # Question ID
        {"requests": ["EVS_R05_2017_ENG_GB_8", "EVS_R05_2017_ENG_GB_2"], 
        "responses": ["EVS_R05_2017_ENG_GB_3", "EVS_R05_2017_ENG_GB_4", "EVS_R05_2017_ENG_GB_5", "EVS_R05_2017_ENG_GB_6"], 
        "type": "Likert"}, 
    ...
    }   
# Dictionary of translations
 "translations": 
    {'EVS_R05_2017_ENG_GB_1': 
        {'ENG_GB': 'Please indicate how important is in your life',
        'FRE_FR': 'Veuillez indiquer dans quelle mesure cet élément est important dans votre vie:',
        'NOR_NO': 'Si hvor viktig dette er i ditt liv:',
        'POR_PT': 'Por favor indique a importância na sua vido do',
        'GER_DE': 'Bitte geben Sie an, wie wichtig Folgendes in Ihrem Leben ist:',
        'RUS_RU': 'Скажите, пожалуйста, какое значение в Вашей жизни имеет?',
        'CZE_CZ': 'Prosím řekněte, pro každou z následujících skutečností, jak jsou ve Vašem životě důležité:',
        'SPA_ES': 'Por favor, indique cuánta importancia tiene esto en su vida:'},
    ...
    }
}
```

All other files can be **regenerated** from this file.

------------------------------------------------------------------------

## mevs_parallel_corpus.csv

This file is a parallel multilingual corpus of all survey items.

Each row corresponds to a survey item, which is a **translation unit** (question sentence or answer option). Wording may vary and slight semantic variations may occur, due to the context of the human translation (national administration of the EVS).

Example:
| item_id                     | qid | type     | position | ENG_GB                                              | FRE_FR                                                        | NOR_NO                                   | POR_PT                                                                 | GER_DE                                                        | RUS_RU                                                      | CZE_CZ                                                                 | SPA_ES                                           |
|----------------------------|-----|----------|----------|-----------------------------------------------------|---------------------------------------------------------------|------------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------|--------------------------------------------------------------|------------------------------------------------------------------------|--------------------------------------------------|
| EVS_R05_2017_ENG_GB_8      | 0   | request  | 0        | Please indicate how important this is in your life: | Veuillez indiquer dans quelle mesure cet élément est important dans votre vie: | Si hvor viktig dette er i ditt liv:      | Por favor indique a importância que atribui a cada um dos seguintes aspectos da sua vida: | Bitte geben Sie an, wie wichtig Folgendes in Ihrem Leben ist: | Просьба указать, насколько это важно в Вашей жизни: | Prosím řekněte, pro každou z následujících skutečností, jak jsou ve Vašem životě důležité | Por favor, indique cuánta importancia tiene esto en su vida: |
| EVS_R05_2017_ENG_GB_2      | 0   | request  | 1        | Work                                                | Travail                                                       | Arbeid                                   | Trabalho                                                               | Arbeit                                                       | Работа                                                     | Práce                                                                 | Trabajo                                         |
| EVS_R05_2017_ENG_GB_3      | 0   | response | 0        | Very important                                      | Très important                                                | Svært viktig                             | Muito importante                                                       | Sehr wichtig                                                 | Очень важно                                                | Velmi důležitý                                                      | Muy importante                                   |
| EVS_R05_2017_ENG_GB_4      | 0   | response | 1        | Quite important                                     | Assez important                                               | Ganske viktig                            | Bastante importante                                                    | Ziemlich wichtig                                             | Довольно важно                                            | Docela důležitá                                                   | Bastante importante                              |
| EVS_R05_2017_ENG_GB_5      | 0   | response | 2        | Not important                                       | Pas très important                                            | Ikke viktig                              | Pouco importante                                                       | Nicht wichtig                                                | Не очень важно                                            | Vůbec ne důležitý                                                  | No muy importante                                |
| EVS_R05_2017_ENG_GB_6      | 0   | response | 3        | Not at all important                                | Pas important du tout                                         | Slett ikke viktig                        | Nada importante                                                        | Überhaupt nicht wichtig                                      | Совсем не важно                                            | Vůbec ne důležitý                                                  | No es en absoluto importante                      |



------------------------------------------------------------------------

## mevs_prompts_default.csv

This file contains a version of prompts for the sake of example.

Each row contains a **fully formatted survey prompt**, such as the following:

| id  | language | text |
|-----|----------|------|
| 126 | ENG_GB | Please indicate if you think that the British government should or should not have the right to<br>Collect information about anyone living in Great Britain without their knowledge<br>A. Definitely should have the right<br>B. Probably should have the right<br>C. Probably should not have the right<br>D. Definitely should not have the right<br>Answer: |

These prompts use:

-   letter symbols ('letters')
-   canonical answer order (e.g.: '0-1-2-3-4')
-   no tail character ('none')

------------------------------------------------------------------------

# Generating prompts

Prompt construction is implemented in:

    mevs/generator.py

Example usage:

``` python
import json
from mevs.generator import generate_question_string

with open("data/MEVS.json", encoding="utf-8") as f:
    mevs = json.load(f)

prompt = generate_question_string(
    mevs,
    qid="41",
    language="ENG_GB"
)

print(prompt)

# How much do you agree or disagree with this statement?
# When jobs are scarce, men have more right to a job than women
# A. Agree strongly
# B. Agree
# C. Neither agree nor disagree
# D. Disagree
# E. Disagree strongly
# Answer:
```

------------------------------------------------------------------------

# Prompt parameters

The generator allows controlled variation of prompt formatting.

| Parameter   | Description                                      |
|------------|--------------------------------------------------|
| language   | Language of the prompt                           |
| order_code | Permutation of answer options                    |
| symbols    | Answer labeling system (letters, numbers, custom)|
| tail_char  | Character after the answer tag                   |

Example:

``` python
generate_question_string(
    mevs,
    qid="13",
    language="FRE_FR",
    order_code="2-1-0-3",
    symbols="letters",
    tail_char="newline"
)
# "Êtes-vous d'accord ou pas d'accord avec cette affirmation?\nPour développer pleinement ses capacités, il faut avoir un travail\nA. Ni d'accord, ni pas d'accord\nB. Plutôt d'accord\nC. Tout à fait d'accord\nD. Plutôt pas d'accord\nE. Pas du tout d'accord\nRéponse :\n"
```
------------------------------------------------------------------------

# Regenerating the CSV files

The CSV files can be regenerated with:

    python mevs/build_parallel_csv.py
    python mevs/build_default_prompts.py

------------------------------------------------------------------------

# License

The MEVS corpus is derived from the Multilingual Corpus of Survey Questionnaires (MCSQ),
which is distributed under the Creative Commons Attribution–NonCommercial–ShareAlike
4.0 International license.

Accordingly, this dataset is released under the same license:

CC BY-NC-SA 4.0
https://creativecommons.org/licenses/by-nc-sa/4.0/

------------------------------------------------------------------------

# Citation

If you use this corpus, please cite:

    @inproceedings{labat-etal-2026-polyglots,
    title = "Polyglots or Multitudes? Multilingual {LLM} Answers to Value-laden Multiple-Choice Questions",
    author = "Labat, L{\'e}o  and
      Ollion, Etienne  and
      Yvon, Fran{\c{c}}ois",
    editor = "Demberg, Vera  and
      Inui, Kentaro  and
      Marquez, Llu{\'i}s",
    booktitle = "Proceedings of the 19th Conference of the {E}uropean Chapter of the {A}ssociation for {C}omputational {L}inguistics (Volume 1: Long Papers)",
    month = mar,
    year = "2026",
    address = "Rabat, Morocco",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.eacl-long.156/",
    pages = "3382--3398",
    ISBN = "979-8-89176-380-7",
    }
