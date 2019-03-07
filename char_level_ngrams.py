# Char-level n-grams
#
# References:
# -   https://gist.github.com/joe-sullivan/fe8f486fc23ee51db14e56a7a2141c59
# -   https://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139

from collections import *
from random import random

from export_review_data import get_output_file_name


def train_char_lm(fname, order=4):
    with open(fname, 'r', encoding='utf-8') as f:
        data = f.read()
    lm = defaultdict(Counter)
    pad = '~' * order
    data = pad + data
    for i in range(len(data) - order):
        history, char = data[i:i + order], data[i + order]
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
        if x <= 0: return c


def generate_text(lm, order, nletters=1000):
    history = '~' * order
    out = []
    for _ in range(nletters):
        c = generate_letter(lm, history, order)
        history = history[-order:] + c
        out.append(c)
    return ''.join(out)


if __name__ == '__main__':
    order = 20
    lm = train_char_lm(get_output_file_name(), order=order)
    print(generate_text(lm, order))
