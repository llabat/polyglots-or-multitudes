import os
import sys
import math
import argparse
import itertools
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from mcp import run_mcp_batch
from mevs.generator import generate_question_string
from utils import load_config, load_mevs, load_completed_answerids, expand_orders, build_answerid, load_model

def process_batch(batch, model, tokenizer, model_name, output_file):
    prompts = [b["prompt"] for b in batch]
    answer_tokens = [b["answer_tokens"] for b in batch]

    choices = run_mcp_batch(prompts, answer_tokens, model, tokenizer)

    rows = []
    for b, p, choice in zip(batch, prompts, choices):
        rows.append({
            "answerid": b["answerid"],
            "prompt": p,
            #"model": model_name,
            #"qid": b["qid"],
            #"language": b["lang"],
            #"symbol": b["symbol"],
            #"tail": b["tail"],
            #"order": b["order"],
            "choice": choice[0],
            "answer": choice[1]
        })

    df = pd.DataFrame(rows)
    df.to_csv(
        output_file,
        mode="a",
        header=not os.path.exists(output_file),
        index=False,
    )


def main(config_path, model_override=None):

    config = load_config(config_path)

    mevs = load_mevs(config["dataset"]["path"])
    questions = config["dataset"]["question_set"]

    languages = config["dataset"]["languages"]
    symbols = config["prompt"]["symbols"]
    tails = config["prompt"]["tail"]
    orders_cfg = config["prompt"]["order"]

    cache_dir = config.get("model_cache", None)
    precision = config.get("precision", 16)

    output_dir = config["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    done_ids = load_completed_answerids(output_dir)
    print(f"Loaded {len(done_ids)} completed combinations")

    model_name = model_override if model_override else config["model"]

    output_file = os.path.join(
        output_dir,
        f"{model_name.replace('/', '_')}.csv"
    )

    model, tokenizer = load_model(model_name, cache_dir, precision)

    BATCH_SIZE = 32
    batch_groups = defaultdict(list)
    combo_factor = len(languages) * len(symbols) * len(tails)

    total = 0
    for qid in questions:
        qid_str = str(qid)
        n_choices = len(mevs["questions"][qid_str]["responses"])

        if orders_cfg == "all":
            n_orders = math.factorial(n_choices)
        else:
            n_orders = len(orders_cfg)

        total += n_orders * combo_factor

    pbar = tqdm(total=total)
    pbar.update(len(done_ids))

    for qid in questions:
        qid_str = str(qid)
        n_choices = len(mevs["questions"][qid_str]["responses"])
        orders = expand_orders(orders_cfg, n_choices)

        for order in orders:
            for lang, symb, tail in itertools.product(languages, symbols, tails):

                answerid = build_answerid(qid_str, model_name, lang, symb, order, tail)

                if answerid in done_ids:
                    continue

                q = generate_question_string(
                    mevs,
                    qid=qid_str,
                    language=lang,
                    order_code=order,
                    symbols=symb,
                    tail_char=tail,
                )
                prompt = q["prompt"]
                answer_set = q["answer_tokens"]

                key = tuple(answer_set)

                batch_groups[key].append({
                    "answerid": answerid,
                    "prompt": prompt,
                    "answer_tokens": answer_set,
                    "qid": qid_str,
                    "lang": lang,
                    "symbol": symb,
                    "tail": tail,
                    "order": order,
                })

                group = batch_groups[key]

                if len(group) >= BATCH_SIZE:
                    process_batch(group, model, tokenizer, model_name, output_file)
                    pbar.update(len(group))
                    batch_groups[key] = []

    # final flush
    for group in batch_groups.values():
        if group:
            process_batch(group, model, tokenizer, model_name, output_file)
            pbar.update(len(group))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file")
    parser.add_argument("--model", help="Model override", default=None)

    args = parser.parse_args()

    main(args.config, model_override=args.model)