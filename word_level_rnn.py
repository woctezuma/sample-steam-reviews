# Reference: https://github.com/rdcolema/word-level-rnn-for-text-generation/blob/master/word_gen.py

import random

import numpy as np
from keras.layers.core import Dense, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.models import model_from_json

from download_review_data import get_artifact_app_id
from export_review_data import get_output_file_name


def get_model_architecture_file_name():
    return 'word_level_rnn_model_architecture.h5'


def get_model_weights_file_name():
    return 'word_level_rnn_model_weights.h5'


def sample(a, temperature=1.0):
    # helper function to sample an index from a probability array
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    if sum(a) > 1.0:  # occasionally getting 1.00000X, so handling for that
        a *= 0.999
    return np.argmax(np.random.multinomial(1, a, 1))


def train(path, maxlen=30):
    """trains the LSTM model on text corpora"""

    try:
        text = open(path).read().lower()
    except UnicodeDecodeError:
        import codecs

        text = codecs.open(path, encoding='utf-8').read().lower()

    print('corpus length: {}'.format(len(text)))

    chars = set(text)
    words = set(text.split())

    print("total number of unique words: {}".format(len(words)))
    print("total number of unique chars: {}".format(len(chars)))

    word_indices = dict((c, i) for i, c in enumerate(words))
    indices_word = dict((i, c) for i, c in enumerate(words))

    step = 3

    print("maxlen: {} ; step: {}".format(maxlen, step))

    sentences = []
    next_words = []
    list_words = text.lower().split()

    for i in range(0, len(list_words) - maxlen, step):
        sentences2 = ' '.join(list_words[i : i + maxlen])
        sentences.append(sentences2)
        next_words.append((list_words[i + maxlen]))

    print('length of sentence list: {}'.format(len(sentences)))
    print("length of next_word list: {}".format(len(next_words)))

    print('Vectorization...')
    X = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
    y = np.zeros((len(sentences), len(words)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, word in enumerate(sentence.split()):
            X[i, t, word_indices[word]] = 1
        y[i, word_indices[next_words[i]]] = 1

    # build the model: 2 stacked LSTM

    print('Building model...')

    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, len(words))))
    model.add(Dropout(0.5))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.5))
    model.add(Dense(len(words), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    try:
        model.load_weights(get_model_weights_file_name())
    except Exception as e:
        print(e)
        pass

    # train the model, output generated text after each iteration

    for iteration in range(1, 750):
        print('Iteration {}'.format(iteration))

        model.fit(X, y, batch_size=500, nb_epoch=3)
        json_string = model.to_json()
        with open(get_model_architecture_file_name(), 'w') as f:
            f.write(json_string)
        model.save_weights(get_model_weights_file_name(), overwrite=True)

    return model


def generate_from_word_level_rnn(
    path,
    maxlen=30,
    diversity=1.0,
    min_sent_len=10,
    max_sent_len=65,
):
    with open(path, "r", encoding='utf-8') as f:
        text = f.read().lower().split()[:4940]
    words = set(text)
    start_index = random.randint(0, len(text) - maxlen - 1)
    word_indices = dict((c, i) for i, c in enumerate(words))
    indices_word = dict((i, c) for i, c in enumerate(words))

    response = ""
    model = model_from_json(open(path).read())
    model.load_weights(get_model_weights_file_name())
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    sentence = text[start_index : start_index + maxlen]

    for i in range(random.randint(min_sent_len, max_sent_len)):
        x = np.zeros((1, maxlen, len(words)))
        for t, word in enumerate(sentence):
            x[0, t, word_indices[word]] = 1.0
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_word = indices_word[next_index]
        if not response:
            response += ' {0}'.format(next_word)
        else:
            if response.split()[-1] != next_word:
                response += ' {0}'.format(next_word)
        del sentence[0]
        sentence.append(next_word)
    return response


def load_model():
    model = model_from_json(open(get_model_architecture_file_name()).read())
    model.load_weights(get_model_weights_file_name())
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    return model


if __name__ == "__main__":
    app_id = get_artifact_app_id()
    text_file_name = get_output_file_name(app_id)
    model = train(path=text_file_name)
    response = generate_from_word_level_rnn(path=text_file_name)
