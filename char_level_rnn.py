# Reference: https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py

'''Example script to generate text from Nietzsche's writings.

At least 20 epochs are required before the generated text
starts sounding coherent.

It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.

If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

import random
import string
import sys

import numpy as np
from keras.callbacks import LambdaCallback, ModelCheckpoint
from keras.layers import LSTM, Dense
from keras.layers.core import Dropout
from keras.models import Sequential, load_model
from keras.utils.data_utils import get_file

from download_review_data import get_artifact_app_id
from export_review_data import get_output_file_name


def read_input(path=None):
    if path is None:
        path = get_file(
            'nietzsche.txt',
            origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt',
        )

    with open(path, encoding='utf-8') as f:
        text = f.read().lower()
    print('corpus length:', len(text))

    return text


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def sample_new_text(sentence, model, params, diversity):
    generated = ''
    generated += sentence
    print('----- Generating with seed: "' + sentence + '"')
    sys.stdout.write(generated)

    maxlen = params['maxlen']
    chars = params['chars']
    char_indices = params['char_indices']
    indices_char = params['indices_char']

    for _i in range(400):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.0

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

        sys.stdout.write(next_char)
        sys.stdout.flush()
    print()

    return


def get_params(maxlen=None):
    chars = string.ascii_letters + string.digits + string.punctuation + ' '

    print('total chars:', len(chars))
    char_indices = {c: i for i, c in enumerate(chars)}
    indices_char = {i: c for i, c in enumerate(chars)}

    params = {}
    params['chars'] = chars
    params['char_indices'] = char_indices
    params['indices_char'] = indices_char

    if maxlen is not None:
        params['maxlen'] = maxlen

    return params


def trim_text(text, chars_to_keep):
    # Remove unusual characters

    text_chars = sorted(list(set(text)))

    chars_to_remove = ''.join(set(text_chars).difference(chars_to_keep))
    print(f'Removing {len(chars_to_remove)} characters: {chars_to_remove}')

    translator = str.maketrans('', '', chars_to_remove)
    trimmed_text = text.translate(translator)

    return trimmed_text


def train_model(
    text,
    maxlen=40,
    num_epochs=60,
    full_model_filename=None,
    initial_epoch=0,
):
    params = get_params(maxlen)

    chars = params['chars']
    char_indices = params['char_indices']
    indices_char = params['indices_char']

    # Remove unusual characters
    text = trim_text(text, chars)

    # cut the text in semi-redundant sequences of maxlen characters
    # maxlen = params['maxlen']
    step = 3
    sentences = []
    next_chars = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i : i + maxlen])
        next_chars.append(text[i + maxlen])
    print('nb sequences:', len(sentences))

    print('Vectorization...')
    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1

    # build the model: a single LSTM
    print('Build model...')
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, len(chars))))
    model.add(Dropout(0.5))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.5))
    model.add(Dense(len(chars), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    def on_epoch_end(epoch, _):
        # Function invoked at end of each epoch. Prints generated text.
        print()
        print('----- Generating text after Epoch: %d' % epoch)

        start_index = random.randint(0, len(text) - maxlen - 1)
        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print('----- diversity:', diversity)

            sentence = text[start_index : start_index + maxlen]
            sample_new_text(sentence, model, params, diversity)

    print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

    save_callback = ModelCheckpoint(
        filepath='model.char_level_rnn.epoch_{epoch:02d}.hdf5',
        save_weights_only=False,
    )

    if full_model_filename is not None:
        try:
            print(
                'Loading model {} with initial epoch = {}'.format(
                    full_model_filename,
                    initial_epoch,
                ),
            )
            model = load_model(full_model_filename)
        except FileNotFoundError:
            print('Model not found. Setting initial epoch to 0.')
            initial_epoch = 0

    model.fit(
        x,
        y,
        batch_size=128,
        epochs=num_epochs,
        initial_epoch=initial_epoch,
        callbacks=[print_callback, save_callback],
    )

    return model


if __name__ == '__main__':
    app_id = get_artifact_app_id()
    text = read_input(get_output_file_name(app_id))

    maxlen = 20
    params = get_params(maxlen)

    text = trim_text(text, params['chars'])

    model = train_model(
        text,
        maxlen,
        num_epochs=20,
        full_model_filename=None,
        initial_epoch=0,
    )

    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print('----- diversity:', diversity)
        sentence = text[start_index : start_index + maxlen]
        sample_new_text(sentence, model, params, diversity)
