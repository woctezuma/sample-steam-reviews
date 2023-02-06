from filter_review_data import (
    get_negative_review_ids,
    get_positive_review_ids,
    load_english_reviews,
)


def get_useful_review_ids(english_review_dict, voted_up=None):
    if voted_up is None:
        review_ids = english_review_dict.keys()
    elif voted_up:
        review_ids = get_positive_review_ids(english_review_dict)
    else:
        review_ids = get_negative_review_ids(english_review_dict)

    useful_review_ids = sorted(
        review_ids,
        key=lambda x: english_review_dict[x]['weighted_vote_score'],
        reverse=True,
    )

    return useful_review_ids


def print_useful_reviews(english_review_dict, verbose=True):
    useful_positive_review_ids = get_useful_review_ids(
        english_review_dict,
        voted_up=True,
    )
    useful_negative_review_ids = get_useful_review_ids(
        english_review_dict,
        voted_up=False,
    )

    the_most_useful_positive_review = english_review_dict[
        useful_positive_review_ids[0]
    ]['review']
    the_most_useful_negative_review = english_review_dict[
        useful_negative_review_ids[0]
    ]['review']

    print(
        'The most useful positive review: {} characters'.format(
            len(the_most_useful_positive_review),
        ),
    )
    print(
        'The most useful negative review: {} characters'.format(
            len(the_most_useful_negative_review),
        ),
    )

    if verbose:
        print('\n[POSITIVE]\n----------\n')
        print(the_most_useful_positive_review)
        print('\n[NEGATIVE]\n----------\n')
        print(the_most_useful_negative_review)

    return


if __name__ == '__main__':
    english_review_dict = load_english_reviews()
    print_useful_reviews(english_review_dict)
