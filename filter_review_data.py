from download_review_data import load_reviews


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


def load_english_reviews(language_str='english', verbose=True):
    review_dict = load_reviews()

    languages = cluster_reviews_by_language(review_dict)

    english_review_dict = dict()
    for is_upvote in [True, False]:
        for review_id in languages[language_str][is_upvote]:
            review_text = review_dict['reviews'][review_id]['review']
            review_usefulness = float(review_dict['reviews'][review_id]['weighted_vote_score'])

            english_review_dict[review_id] = dict()
            english_review_dict[review_id]['review'] = review_text
            english_review_dict[review_id]['voted_up'] = is_upvote
            english_review_dict[review_id]['weighted_vote_score'] = review_usefulness

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

    print('Filtering out reviews with strictly fewer than {} characters.'.format(length_threshold))
    review_ids = filter(lambda x: len(english_review_dict[x]['review']) >= length_threshold, review_ids)

    long_english_review_dict = dict()
    for review_id in review_ids:
        long_english_review_dict[review_id] = dict()
        long_english_review_dict[review_id] = english_review_dict[review_id]

    return long_english_review_dict


if __name__ == '__main__':
    english_review_dict = load_english_reviews()
    english_review_dict = filter_out_short_reviews(english_review_dict, length_threshold=150)
