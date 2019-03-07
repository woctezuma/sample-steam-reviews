# Sample Steam Reviews

[![Build status][build-image]][build]
[![Updates][dependency-image]][pyup]
[![Python 3][python3-image]][pyup]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to sample Steam reviews for the games called [Artifact](https://store.steampowered.com/app/583950/Artifact/).


## Requirements

-   Install the latest version of [Python 3.X](https://www.python.org/downloads/). For CNTK, you will need Python 3.6.
-   Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Download Steam reviews for Artifact and for the top 100 most played games in the past 4 weeks

```
python download_review_data.py
```

### Extract English reviews

```
python filter_review_data.py
```

### Concatenate filtered reviews in a large text file

```
python export_review_data.py
```

### Display info about reviews

```
python display_review_data.py
python sort_review_data.py
```

### Learn char-level models

```
# Char-level n-grams:
python char_level_ngrams.py

# Char-level RNN: either run this script, or the `char_level_rnn.ipynb` notebook on Google Colab. 
python char_level_rnn.py
```

### Learn word-level models

**Caveat**: this does not work for now (too much RAM used due to one-hot encoding of words).

```
# Word-level RNN: either run this script, or the `word_level_rnn.ipynb` notebook on Google Colab. 
python word_level_rnn.py
```

### Learn word-level models with GloVe embeddings

```
# Word-level RNN with embeddings: either run this script, or `word_level_rnn_with_embeddings.ipynb` on Google Colab. 
python word_level_rnn_with_embeddings.py
```

### Download app details for Artifact and for the top 100 most played games in the past 4 weeks

If generated reviews look satisfactory, then the next step would be to generate a review given a store description using
[Sequence-to-Sequence learning](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html).
For this purpose, we download app details, which contain store descriptions. 

```
python download_app_data.py
```

## Results

TODO

## References

-   [Andrej Karpathy, "The Unreasonable Effectiveness of Recurrent Neural Networks", 2015](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
-   [Yoav Goldberg, "Character-level Language Models", 2015](https://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139)
-   [Keras: word-embeddings](https://blog.keras.io/using-pre-trained-word-embeddings-in-a-keras-model.html)
-   [StackOverflow: word-embeddings for word-level RNN](https://stackoverflow.com/a/48230654)
-   [Keras: sequence-to-sequence learning](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html)

[build]: <https://travis-ci.org/woctezuma/sample-steam-reviews>
[build-image]: <https://travis-ci.org/woctezuma/sample-steam-reviews.svg?branch=master>

[pyup]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/python-3-shield.svg>

[codecov]: <https://codecov.io/gh/woctezuma/sample-steam-reviews>
[codecov-image]: <https://codecov.io/gh/woctezuma/sample-steam-reviews/branch/master/graph/badge.svg>

[codacy]: <https://www.codacy.com/app/woctezuma/sample-steam-reviews>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/1f8b420b27344e48bfa54dee59d76f62>

