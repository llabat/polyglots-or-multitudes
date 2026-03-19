import torch
import torch.nn.functional as F
from collections import defaultdict


def get_grouped_token_log_probs(model, tokenizer, prompts, answer_tokens_list):
    """
    prompts: List[str]
    answer_tokens_list: List[List[str]] (same length as prompts)
    """

    # Tokenize
    inputs = tokenizer(prompts, return_tensors="pt", padding=True).to(model.device)
    last_token_positions = torch.sum(inputs.attention_mask, dim=1) - 1  # (B,)

    # Forward pass
    with torch.no_grad():
        logits = model(**inputs, use_cache=False).logits  # (B, T, V)

    batch_size, _, vocab_size = logits.shape

    # Extract last-token logits
    last_token_positions = last_token_positions.unsqueeze(-1).expand(-1, vocab_size)
    last_logits = torch.gather(
        logits, 1, last_token_positions.unsqueeze(1)
    ).squeeze(1)  # (B, V)

    # Group by identical answer token sets
    group_map = defaultdict(list)
    for idx, tokens in enumerate(answer_tokens_list):
        group_map[tuple(tokens)].append(idx)

    token_log_probs = [None] * batch_size

    for answer_tokens, indices in group_map.items():
        token_ids = tokenizer.convert_tokens_to_ids(list(answer_tokens))
        indices_tensor = torch.tensor(indices, device=model.device)

        group_logits = last_logits[indices_tensor][:, token_ids]
        group_log_probs = F.log_softmax(group_logits, dim=-1).cpu().tolist()

        for i, q_idx in enumerate(indices):
            token_log_probs[q_idx] = dict(zip(answer_tokens, group_log_probs[i]))

    return token_log_probs


def mcp(token_log_probs):
    return max(token_log_probs, key=lambda i: token_log_probs[i])


def run_mcp_batch(prompts, answer_tokens_list, model, tokenizer):
    token_log_probs = get_grouped_token_log_probs(
        model, tokenizer, prompts, answer_tokens_list
    )
    max_tokens = [mcp(probs) for probs in token_log_probs]
    likert_notches = [answer_tokens_list[i].index(t) for i, t in enumerate(max_tokens)]
    return list(zip(max_tokens, likert_notches))