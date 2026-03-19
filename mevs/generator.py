import json
from mevs.const import SYMBOLS, TAIL_CHARS, ANSWER_DICT

MEVS_PATH = "../data/MEVS.json"

def generate_question_string(mevs, qid, language, order_code = None, symbols = "letters", tail_char = "none"):
    """
    Generate a formatted survey prompt from the MEVS dataset.

    Parameters
    ----------
    mevs : dict
        MEVS dataset object.
    qid : str
        Question identifier.
    language : str
        Language code (e.g., 'ENG_GB').
    order_code : str, optional
        Permutation of answer indices (e.g., "2-0-1-3").
    symbols : str or list
        Symbol system ('letters', 'numbers') or custom list.
    tail_char : str
        Formatting after answer tag ('none', 'newline', 'space').

    Returns
    -------
    str
        Fully formatted survey prompt.
    """
    # Check language
    if language not in ANSWER_DICT:
        raise ValueError(f"Language '{language}' is not supported (must be one of {list(ANSWER_DICT.keys())})")

    # Check tail character
    if tail_char not in TAIL_CHARS:
        raise ValueError(f"tail_char should be one of {list(TAIL_CHARS.keys())}")
    
    # Collect the question
    try:
        question = mevs["questions"][qid]
    except KeyError:
        raise KeyError(f"Question '{qid}' is not in the MEVS.")
    
    # Collect requests and responses
    requests, responses = question['requests'], question['responses']

    # Check order
    order = order_code.split("-") if order_code else [str(i) for i in range(len(responses))]
    if len(order) != len(set(order)):
        raise ValueError(f"order_code must not contain redundant indices (got {order})")

    # Check symbols
    if isinstance(symbols, str):
        if symbols not in SYMBOLS:
            raise ValueError(f"symbols must be one of {list(SYMBOLS.keys())}")
        symbols = SYMBOLS[symbols][:len(order)]
    elif isinstance(symbols, list):
        if len(symbols) != len(order):
            raise ValueError("If symbols is a list, it must contain as many symbols as indices in order_code.")
    else:
        raise Exception(f"symbols should be one of {list(SYMBOLS.keys())} or a list.")

    # Check the cardinality
    if len(responses) != len(order):
        raise ValueError(f"Question {qid} has cardinality {len(responses)} (mismatched order_code {order_code})")

    question_string = ""
    for req_id in requests:
        try:
            question_string += mevs["translations"][req_id][language] + "\n"
        except KeyError:
            raise KeyError(f"Language '{language}' not available  for survey item '{req_id}'")
    
    for i, idx in enumerate(order):
        try:
            question_string += symbols[i] + ". " + mevs["translations"][responses[int(idx)]][language] + "\n"
        except KeyError:
            raise KeyError(
                f"Missing translation for response '{responses[int(idx)]}' in language '{language}'"
            )
    
    question_string = question_string + ANSWER_DICT[language] + TAIL_CHARS[tail_char]

    return {
        "prompt": question_string,
        "answer_tokens": symbols
    }
