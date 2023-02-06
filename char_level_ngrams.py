# Char-level n-grams
#
# References:
# -   https://gist.github.com/joe-sullivan/fe8f486fc23ee51db14e56a7a2141c59
# -   https://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139

import string
from collections import *
from random import random

from download_review_data import get_artifact_app_id
from export_review_data import get_output_file_name


def train_char_lm(fname, order=4):
    with open(fname, 'r', encoding='utf-8') as f:
        data = f.read()
    lm = defaultdict(Counter)
    pad = '~' * order
    data = pad + data
    for i in range(len(data) - order):
        history, char = data[i : i + order], data[i + order]
        lm[history][char] += 1

    def normalize(counter):
        s = float(sum(counter.values()))
        return [(c, cnt / s) for c, cnt in counter.items()]

    outlm = {hist: normalize(chars) for hist, chars in lm.items()}
    return outlm


def generate_letter(lm, history, order):
    history = history[-order:]
    dist = lm[history]
    x = random()
    for c, v in dist:
        x = x - v
        if x <= 0:
            return c


def generate_text(lm, order, nletters=1000):
    history = '~' * order
    out = []
    for _ in range(nletters):
        c = generate_letter(lm, history, order)
        history = history[-order:] + c
        out.append(c)
    return ''.join(out)


def print_corpus_info(app_id=None):
    fname = get_output_file_name(app_id)
    with open(fname, 'r', encoding='utf-8') as f:
        data = f.read()

    print('Corpus size: {} characters (with puncutation).'.format(len(data)))

    # Reference: https://gist.github.com/maxim5/c35ef2238ae708ccb0e55624e9e0252b#gistcomment-2839110
    translator = str.maketrans('', '', string.punctuation)
    data = data.translate(translator)

    print('Corpus size: {} characters (without puncutation).'.format(len(data)))

    return


if __name__ == '__main__':
    app_id = get_artifact_app_id()
    print_corpus_info(app_id)

    order = 20
    lm = train_char_lm(get_output_file_name(app_id), order=order)
    print(generate_text(lm, order))
