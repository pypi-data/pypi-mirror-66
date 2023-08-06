from typing import List


def n_grams(x: List[any], n: int) -> List[tuple]:
    result = []
    for i in range(len(x) - n + 1):
        result.append(tuple(x[i:i + n]))
    return result


def rouge_n(reference: List[any], candidate: List[any], n: int) -> float:
    ref_ngrams = n_grams(reference, n)
    candidate_ngrams = n_grams(candidate, n)

    if len(ref_ngrams) == 0 and len(candidate_ngrams) == 0:
        return 1.0
    elif len(ref_ngrams) == 0 or len(candidate_ngrams) == 0:
        return 0.0

    unique_c = set(candidate_ngrams)

    matches = 0
    for ngram in ref_ngrams:
        if ngram in unique_c:
            matches += 1

    recall = matches / len(ref_ngrams)
    precision = matches / len(candidate_ngrams)

    if precision + recall == 0:
        return 0.0

    f1_score = 2 * precision * recall / (precision + recall)
    return f1_score
