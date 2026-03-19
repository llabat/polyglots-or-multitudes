import json
import pandas as pd

MEVS_PATH = "../data/MEVS.json"
OUT_PATH = "../data/mevs_parallel_corpus.csv"

with open(MEVS_PATH, encoding="utf-8") as f:
    mevs = json.load(f)

rows = []

languages = list(next(iter(mevs["translations"].values())).keys())

for qid, q in mevs["questions"].items():

    for pos, req_id in enumerate(q["requests"]):

        row = {
            "item_id": req_id,
            "qid": qid,
            "type": "request",
            "position": pos
        }

        for lang in languages:
            row[lang] = mevs["translations"][req_id].get(lang)

        rows.append(row)

    for pos, resp_id in enumerate(q["responses"]):

        row = {
            "item_id": resp_id,
            "qid": qid,
            "type": "response",
            "position": pos
        }

        for lang in languages:
            row[lang] = mevs["translations"][resp_id].get(lang)

        rows.append(row)

df = pd.DataFrame(rows)
#df.sort_values(["qid", "type", "position"], inplace=True)

df.to_csv(OUT_PATH, index=False)

print("Exported parallel corpus:", OUT_PATH)