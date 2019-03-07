# References:
# -   Text classification: https://github.com/keras-team/keras/blob/master/examples/pretrained_word_embeddings.py
# -   Text generation: https://gist.github.com/maxim5/c35ef2238ae708ccb0e55624e9e0252b
# -   GloVe embeddings withing spaCy: https://spacy.io/models/en#section-en_vectors_web_lg
# -   GloVe embeddings: https://nlp.stanford.edu/projects/glove/

import string

import numpy as np
import spacy
from keras.callbacks import LambdaCallback
from keras.layers import Dense, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential

from download_review_data import get_artifact_app_id
from export_review_data import get_output_file_name


def chunks(l, n, overlap_size=0):
    # Reference: https://stackoverflow.com/a/36586925/
    # Reference: https://stackoverflow.com/a/312464
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n - overlap_size):
        yield l[i:i + n]


def train_model(path, max_sentence_len=40, overlap_size=0, num_epochs=20):
    if overlap_size is None:
        overlap_size = max_sentence_len - 1

    assert (0 <= overlap_size < max_sentence_len)

    print('\nLoading GloVe...')
    nlp = spacy.load('en_vectors_web_lg')
    word_model = nlp.vocab
    pretrained_weights = word_model.vectors.data
    vocab_size, emdedding_size = pretrained_weights.shape
    print('Result embedding shape:', pretrained_weights.shape)

    def word2idx(my_word):
        my_key = word_model.strings[my_word]
        try:
            my_row = word_model.vectors.key2row[my_key]
        except KeyError:
            print('Word {} unknown'.format(my_word))
            my_row = 2091  # the row for 'cat' word
        return my_row

    def idx2word(my_row):
        my_key = list(word_model.vectors.keys())[my_row]
        my_word = word_model.strings[my_key]
        return my_word

    print('\nPreparing the sentences...')

    with open(path, 'r', encoding='utf-8') as f:
        docs = f.readlines()
    translator = str.maketrans('', '', string.punctuation)
    sentences = []
    for doc in docs:
        tokens = [word for word in doc.lower().translate(translator).split()
                  if word_model.has_vector(word)]
        current_sentences = [sentence for sentence in chunks(tokens, max_sentence_len, overlap_size)
                             if len(sentence) > 1]
        sentences.extend(current_sentences)
    print('Num sentences:', len(sentences))

    print('\nPreparing the data for LSTM...')
    train_x = np.zeros([len(sentences), max_sentence_len], dtype=np.int32)
    train_y = np.zeros([len(sentences)], dtype=np.int32)
    for i, sentence in enumerate(sentences):
        for t, word in enumerate(sentence[:-1]):
            train_x[i, t] = word2idx(word)
            train_y[i] = word2idx(sentence[-1])
    print('train_x shape:', train_x.shape)
    print('train_y shape:', train_y.shape)

    print('\nTraining LSTM...')
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=emdedding_size, weights=[pretrained_weights]))
    model.add(LSTM(units=emdedding_size))
    model.add(Dense(units=vocab_size))
    model.add(Activation('softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

    def sample(preds, temperature=1.0):
        if temperature <= 0:
            return np.argmax(preds)
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def generate_next(text, num_generated=10):
        word_idxs = [word2idx(word) for word in text.lower().split()]
        for i in range(num_generated):
            prediction = model.predict(x=np.array(word_idxs))
            idx = sample(prediction[-1], temperature=0.7)
            word_idxs.append(idx)
        return ' '.join(idx2word(idx) for idx in word_idxs)

    def on_epoch_end(epoch, _):
        print('\nGenerating text after epoch: %d' % epoch)
        texts = [
            'i like this game because',
            'i do not like this game because',
            'the',
            'a',
        ]
        for text in texts:
            sample = generate_next(text)
            print('%s... -> %s' % (text, sample))

    model.fit(train_x, train_y,
              batch_size=128,
              epochs=num_epochs,
              callbacks=[LambdaCallback(on_epoch_end=on_epoch_end)])

    return model


if __name__ == "__main__":
    # Caveat: you need to first run the following command in the terminal:
    #    python -m spacy download en_vectors_web_lg

    app_id = get_artifact_app_id()
    text_file_name = get_output_file_name(app_id)
    model = train_model(path=text_file_name, max_sentence_len=40, overlap_size=20)