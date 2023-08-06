from typing import List


def n_grams(x: List[any], n: int) -> List[tuple]:
    result = []
    for i in range(len(x) - n + 1):
        result.append(tuple(x[i:i + n]))
    return result


def rouge_n(reference: List[any], candidate: List[any], n: int) -> float:
    if len(reference) == 0 and len(candidate) == 0:
        return 1
    elif len(reference) == 0 or len(candidate) == 0:
        return 0

    ref_ngrams = n_grams(reference, n)
    candidate_ngrams = n_grams(candidate, n)
    unique_c = set(candidate_ngrams)

    matches = 0
    for ngram in ref_ngrams:
        if ngram in unique_c:
            matches += 1

    recall = matches / len(ref_ngrams)
    precision = matches / len(candidate_ngrams)

    f1_score = 2 * precision * recall / (precision + recall)
    return f1_score
