import json
import pandas as pd

from generator import generate_question_string
from const import ANSWER_DICT

MEVS_PATH = "../data/MEVS.json"
OUT_PATH = "../data/mevs_prompts_default.csv"

with open(MEVS_PATH, encoding="utf-8") as f:
    mevs = json.load(f)

rows = []

for qid in mevs["questions"]:

    for language in ANSWER_DICT:

        prompt = generate_question_string(
            mevs,
            qid=qid,
            language=language,
            symbols="letters",
            tail_char="none"
        )

        rows.append({
            "qid": qid,
            "language": language,
            "prompt": prompt
        })

df = pd.DataFrame(rows)
df.to_csv(OUT_PATH, index=False)

print("Exported prompts:", OUT_PATH)