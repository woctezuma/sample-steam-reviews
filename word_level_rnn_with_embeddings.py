# References:
# -   Text classification: https://github.com/keras-team/keras/blob/master/examples/pretrained_word_embeddings.py
# -   Text generation: https://gist.github.com/maxim5/c35ef2238ae708ccb0e55624e9e0252b
# -   GloVe embeddings withing spaCy: https://spacy.io/models/en#section-en_vectors_web_lg
# -   GloVe embeddings: https://nlp.stanford.edu/projects/glove/

import string

import numpy as np
import spacy
from keras.callbacks import LambdaCallback, ModelCheckpoint
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


def train_model(path, max_sentence_len=40, overlap_size=0, num_epochs=20, model_weights_filename=None, initial_epoch=0):
    if overlap_size is None:
        overlap_size = max_sentence_len - 1

    assert (0 <= overlap_size < max_sentence_len)

    print('\nLoading GloVe...')
    nlp = spacy.load('en_vectors_web_lg')
    word_model = nlp.vocab

    print('\nPreparing the sentences...')

    data_driven_vocabulary = set()

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

        data_driven_vocabulary = data_driven_vocabulary.union(tokens)

    num_unique_words = len(data_driven_vocabulary)

    print('Num sentences: {}'.format(len(sentences)))
    print('Num unique words: {}'.format(num_unique_words))

    # Work on the full GloVe matrix

    true_pretrained_weights = word_model.vectors.data

    num_word_features = true_pretrained_weights.shape[1]

    def true_word2idx(my_word):
        my_key = word_model.strings[my_word]
        try:
            my_row = word_model.vectors.key2row[my_key]
        except KeyError:
            print('Word {} unknown'.format(my_word))
            my_row = 2091  # the row for 'cat' word
        return my_row

    def true_idx2word(my_row):
        my_key = list(word_model.vectors.keys())[my_row]
        my_word = word_model.strings[my_key]
        return my_word

    # Trim the GloVe matrix to lower RAM usage

    sorted_data_driven_vocabulary = sorted(list(data_driven_vocabulary))

    word_indices = dict((c, i) for i, c in enumerate(sorted_data_driven_vocabulary))
    indices_word = dict((i, c) for i, c in enumerate(sorted_data_driven_vocabulary))

    def word2idx(my_word):
        return word_indices[my_word]

    def idx2word(my_row):
        return indices_word[my_row]

    pretrained_weights = np.zeros((num_unique_words, num_word_features))
    for my_row in range(num_unique_words):
        true_row = true_word2idx(idx2word(my_row))
        pretrained_weights[my_row] = true_pretrained_weights[true_row, :]

    vocab_size, emdedding_size = pretrained_weights.shape
    print('Result embedding shape:', pretrained_weights.shape)

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

    print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

    save_callback = ModelCheckpoint(filepath='weights.word_level_rnn_with_embeddings.epoch_{epoch:02d}.hdf5',
                                    save_weights_only=True)

    if model_weights_filename is not None:
        try:
            print('Loading model weights {} with initial epoch = {}'.format(model_weights_filename, initial_epoch))
            model.load_weights(model_weights_filename)
        except FileNotFoundError:
            print('Model weights not found. Setting initial epoch to 0.')
            initial_epoch = 0

    model.fit(train_x, train_y,
              batch_size=128,
              epochs=num_epochs,
              initial_epoch=initial_epoch,
              callbacks=[print_callback, save_callback])

    return model


if __name__ == "__main__":
    # Caveat: you need to first run the following command in the terminal:
    #    python -m spacy download en_vectors_web_lg

    app_id = get_artifact_app_id()
    text_file_name = get_output_file_name(app_id)
    model = train_model(path=text_file_name,
                        max_sentence_len=40,
                        overlap_size=35,
                        num_epochs=20,
                        model_weights_filename=None,
                        initial_epoch=0)
