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


def get_useful_reviews(english_review_dict, voted_up=None, length_threshold=150):
    review_ids = english_review_dict.keys()

    print('Filtering out reviews with strictly fewer than {} characters.'.format(length_threshold))
    review_ids = filter(lambda x: len(english_review_dict[x]['review']) >= length_threshold, review_ids)

    if voted_up is None:
        pass
    elif voted_up:
        review_ids = filter(lambda x: english_review_dict[x]['voted_up'], review_ids)
    else:
        review_ids = filter(lambda x: not english_review_dict[x]['voted_up'], review_ids)

    useful_review_ids = sorted(review_ids,
                               key=lambda x: english_review_dict[x]['weighted_vote_score'],
                               reverse=True)

    return useful_review_ids


def print_useful_reviews(english_review_dict, verbose=True):
    useful_positive_review_ids = get_useful_reviews(english_review_dict, voted_up=True)
    useful_negative_review_ids = get_useful_reviews(english_review_dict, voted_up=False)

    the_most_useful_positive_review = english_review_dict[useful_positive_review_ids[0]]['review']
    print('\nThe most useful positive review: {} characters\n'.format(len(the_most_useful_positive_review)))
    if verbose:
        print(the_most_useful_positive_review)

    the_most_useful_negative_review = english_review_dict[useful_negative_review_ids[0]]['review']
    print('\nThe most useful negative review: {} characters\n'.format(len(the_most_useful_negative_review)))
    if verbose:
        print(the_most_useful_negative_review)

    return


if __name__ == '__main__':
    english_review_dict = load_english_reviews()
    print_useful_reviews(english_review_dict)
