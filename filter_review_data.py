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
            english_review_dict[review_id] = dict()
            english_review_dict[review_id]['review'] = review_dict['reviews'][review_id]['review']
            english_review_dict[review_id]['voted_up'] = is_upvote

    if verbose:
        print('Loading {} English reviews.'.format(len(english_review_dict)))

    return english_review_dict


if __name__ == '__main__':
    english_review_dict = load_english_reviews()
