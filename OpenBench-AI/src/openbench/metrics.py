import re
from collections import Counter

def normalize(text: str) -> str:
    """Normalize whitespace and case for a simple baseline comparison."""
    return re.sub(r"\s+", " ", text.strip().lower())

def exact_match(prediction: str, reference: str) -> float:
    return float(normalize(prediction) == normalize(reference))

def token_f1(prediction: str, reference: str) -> float:
    """Whitespace-token F1 baseline; not a semantic correctness measure."""
    pred_tokens = normalize(prediction).split()
    ref_tokens = normalize(reference).split()
    if not pred_tokens and not ref_tokens:
        return 1.0
    if not pred_tokens or not ref_tokens:
        return 0.0
    overlap = sum((Counter(pred_tokens) & Counter(ref_tokens)).values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred_tokens)
    recall = overlap / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)
