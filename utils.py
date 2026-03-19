import os
import json
import yaml
import torch
import random
import logging
import itertools
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_mevs(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def expand_orders(order_config, n_choices):
    base_indices = [str(i) for i in range(n_choices)]

    orders = []

    for mode in order_config:
        if mode == "default":
            orders.append("-".join(base_indices))

        elif mode == "random":
            shuffled = base_indices[:]
            random.shuffle(shuffled)
            orders.append("-".join(shuffled))

        elif mode == "all":
            perms = itertools.permutations(base_indices)
            orders.extend(["-".join(p) for p in perms])

        else:
            raise ValueError(f"Unknown order mode: {mode}")

    return orders


def build_answerid(qid, model, lang, symbol, order, tail):
    return f"{qid}+{model}+{lang}+{symbol}+{order}+{tail}"


def load_completed_answerids(result_dir):
    done = set()

    if not os.path.exists(result_dir):
        return done

    for fname in os.listdir(result_dir):
        if not fname.endswith(".csv"):
            continue

        path = os.path.join(result_dir, fname)
        df = pd.read_csv(path)

        if "answerid" not in df.columns:
            raise ValueError(f"{fname} missing 'answerid' column")

        done.update(df["answerid"].dropna().astype(str))

    return done


def load_model(model_name: str, cache_dir: str = None, precision_bits: int = 16):
    logging.info(f"Loading model: {model_name}")

    model_path = model_name if cache_dir is None else cache_dir + model_name

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype={
            32: torch.float32,
            16: torch.float16,
            8: torch.int8
        }.get(precision_bits, torch.float16)
    )

    logging.info(f"Model {model_name} loaded successfully.")

    return model, tokenizer