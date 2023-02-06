import json
from pathlib import Path

import steamspypi
from langdetect import detect, DetectorFactory, lang_detect_exception

from download_review_data import load_reviews, get_artifact_app_id


def cluster_reviews_by_language(review_dict, verbose=False):
    reviews = review_dict['reviews']

    if verbose:
        print('#downloaded reviews = {}'.format(len(reviews)))

    languages = dict()

    for review_id in reviews:
        language = reviews[review_id]['language']
        voted_up = reviews[review_id]['voted_up']

        if language not in languages:
            languages[language] = dict()
            for is_upvote in [True, False]:
                languages[language][is_upvote] = []

        languages[language][voted_up].append(review_id)

    return languages


def load_english_reviews(app_id=None, language_str='english', verbose=True):
    review_dict = load_reviews(app_id)

    languages = cluster_reviews_by_language(review_dict)

    english_review_dict = dict()
    for is_upvote in [True, False]:
        try:
            for review_id in languages[language_str][is_upvote]:
                review_text = review_dict['reviews'][review_id]['review']
                review_usefulness = float(
                    review_dict['reviews'][review_id]['weighted_vote_score'],
                )

                english_review_dict[review_id] = dict()
                english_review_dict[review_id]['review'] = review_text
                english_review_dict[review_id]['voted_up'] = is_upvote
                english_review_dict[review_id][
                    'weighted_vote_score'
                ] = review_usefulness
        except KeyError:
            continue

    if verbose:
        print('Loading {} English reviews.'.format(len(english_review_dict)))

    return english_review_dict


def get_positive_review_ids(english_review_dict):
    review_ids = english_review_dict.keys()

    review_ids = filter(lambda x: english_review_dict[x]['voted_up'], review_ids)

    return review_ids


def get_negative_review_ids(english_review_dict):
    review_ids = english_review_dict.keys()

    review_ids = filter(lambda x: not english_review_dict[x]['voted_up'], review_ids)

    return review_ids


def filter_out_short_reviews(english_review_dict, length_threshold=150):
    review_ids = english_review_dict.keys()

    print(
        'Filtering out reviews with strictly fewer than {} characters.'.format(
            length_threshold,
        ),
    )
    review_ids = filter(
        lambda x: len(english_review_dict[x]['review']) >= length_threshold,
        review_ids,
    )

    long_english_review_dict = dict()
    for review_id in review_ids:
        long_english_review_dict[review_id] = dict()
        long_english_review_dict[review_id] = english_review_dict[review_id]

    return long_english_review_dict


def get_language_folder_name():
    language_folder = 'data/detected_languages/'
    Path(language_folder).mkdir(parents=True, exist_ok=True)
    return language_folder


def get_language_file_name(app_id=None):
    if app_id is None:
        app_id = get_artifact_app_id()

    file_extension = '.json'
    language_file_name = get_language_folder_name() + str(app_id) + file_extension
    return language_file_name


def detect_review_language(app_id=None, verbose=False):
    english_review_dict = load_english_reviews(app_id)
    output_file_name = get_language_file_name(app_id)

    try:
        with open(output_file_name, 'r', encoding='utf8') as f:
            detected_languages = json.load(f)
    except FileNotFoundError:
        detected_languages = dict()

    DetectorFactory.seed = 0

    is_new_review_processed = False

    for count, review_id in enumerate(english_review_dict):
        if verbose and (count + 1) % 1000 == 0:
            print(
                'Reviews processed by langdetect: {}/{}.'.format(
                    count + 1,
                    len(english_review_dict),
                ),
            )

        if review_id in detected_languages:
            continue

        review_content = english_review_dict[review_id]['review']
        is_new_review_processed = True

        try:
            detected_languages[review_id] = detect(review_content)
        except lang_detect_exception.LangDetectException:
            detected_languages[review_id] = 'unknown'
            print(review_content)

    if is_new_review_processed:
        with open(output_file_name, 'w', encoding='utf8') as f:
            json.dump(detected_languages, f)

    return detected_languages


def detect_review_language_for_top_100(verbose=True):
    data_request = dict()
    data_request['request'] = 'top100in2weeks'
    data = steamspypi.download(data_request)

    app_ids = list(data.keys())

    for app_id in app_ids:
        _ = detect_review_language(app_id, verbose=verbose)

    return


def apply_language_detector():
    # Pre-processing: detect languages of reviews for Artifact and for top 100 most played games

    # Artifact
    detected_languages = detect_review_language(verbose=True)

    # Top 100
    detect_review_language_for_top_100(verbose=True)

    print('Done.\n')

    return


def filter_out_reviews_not_detected_as_english(
    english_review_dict,
    detected_languages,
    expected_language_code='en',
):
    review_ids = english_review_dict.keys()

    print(
        'Filtering out reviews which were not detected as {}.'.format(
            expected_language_code,
        ),
    )
    review_ids = filter(
        lambda x: detected_languages[x] == expected_language_code,
        review_ids,
    )

    checked_english_review_dict = dict()
    for review_id in review_ids:
        checked_english_review_dict[review_id] = dict()
        checked_english_review_dict[review_id] = english_review_dict[review_id]

    return checked_english_review_dict


def filter_reviews(app_id=None):
    if app_id is None:
        app_id = get_artifact_app_id()

    english_review_dict = load_english_reviews(app_id)

    english_review_dict = filter_out_short_reviews(
        english_review_dict,
        length_threshold=150,
    )
    print('#reviews = {}'.format(len(english_review_dict)))

    detected_languages = detect_review_language(app_id)
    english_review_dict = filter_out_reviews_not_detected_as_english(
        english_review_dict,
        detected_languages,
    )
    print('#reviews = {}'.format(len(english_review_dict)))

    return english_review_dict


def main():
    # Pre-processing (only required once)
    apply_language_detector()

    # Processing: Artifact
    app_id = get_artifact_app_id()
    english_review_dict = filter_reviews(app_id)

    return


if __name__ == '__main__':
    main()
