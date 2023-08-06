from typing import List, Optional

from nltk.tokenize import sent_tokenize, word_tokenize
from official.nlp.bert.tokenization import FullTokenizer

from bavard.metrics.rouge import rouge_n
from bavard.text_summarization.extractive.bert.input_features import InputFeatures


def get_rouge_n_score(sentence: str, summary: str, n=2) -> float:
    summary_words = word_tokenize(summary)
    sentence_words = word_tokenize(sentence)
    score = rouge_n(summary_words, sentence_words, n=n)
    return score


def raw_input_to_features(tokenizer: FullTokenizer,
                          article: str,
                          max_seq_len: int,
                          max_sentences: int,
                          is_training: bool,
                          summary: Optional[str] = None) -> InputFeatures:
    if is_training:
        assert summary is not None

    article_sentences = sent_tokenize(article)

    input_tokens = []
    cls_indices = []
    segment_ids = []
    cls_mask = []
    cls_outputs = None

    if is_training:
        cls_outputs = []

    for i, sent in enumerate(article_sentences):
        if i == max_sentences:
            break

        sent_tokens = tokenizer.tokenize(sent)
        assert len(sent_tokens) > 0
        if len(input_tokens) + len(sent_tokens) + 2 > max_seq_len:
            break

        input_tokens += ['[CLS]'] + sent_tokens
        segment_ids += [i % 2] * (len(sent_tokens) + 1)
        cls_indices.append(i)
        cls_mask.append(1)

        if is_training:
            sentence_score = get_rouge_n_score(sent, summary, n=2)
            cls_outputs.append(sentence_score)

    input_tokens.append('[SEP]')
    segment_ids.append(segment_ids[-1])
    input_ids = tokenizer.convert_tokens_to_ids(input_tokens)
    input_mask = [1] * len(input_ids)

    assert len(segment_ids) == len(input_ids) == len(input_mask)
    while len(segment_ids) < max_seq_len:
        input_ids.append(0)
        segment_ids.append(0)
        input_mask.append(0)
    assert len(segment_ids) == len(input_ids) == len(input_mask) == max_seq_len

    assert len(cls_indices) == len(cls_mask)
    while len(cls_indices) < max_sentences:
        cls_indices.append(0)
        cls_mask.append(0)

        if is_training:
            cls_outputs.append(0)
    assert len(cls_indices) == len(cls_mask) == max_sentences

    if is_training:
        assert len(cls_outputs) == max_sentences
    else:
        assert cls_outputs is None

    return InputFeatures(tokens=input_tokens,
                         input_ids=input_ids,
                         input_mask=input_mask,
                         segment_ids=segment_ids,
                         cls_indices=cls_indices,
                         cls_outputs=cls_outputs,
                         cls_mask=cls_mask)
