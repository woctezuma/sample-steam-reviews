from download_review_data import load_reviews
from filter_review_data import cluster_reviews_by_language


def print_global_summary(review_dict):
    query_summary = review_dict['query_summary']

    positive = query_summary['total_positive']
    negative = query_summary['total_negative']

    print(
        'Review score = {} ({})'.format(
            query_summary['review_score'],
            query_summary['review_score_desc'],
        ),
    )
    print('#positive reviews = {}'.format(positive))
    print('#negative reviews = {}'.format(negative))
    print('#reviews = {}'.format(query_summary['total_reviews']))

    if query_summary['total_reviews'] != (positive + negative):
        raise AssertionError()

    return


def print_regional_summary(review_dict):
    languages = cluster_reviews_by_language(review_dict, verbose=True)

    for language in sorted(
        languages.keys(),
        key=lambda x: sum(len(languages[x][is_upvote]) for is_upvote in [True, False]),
    ):
        language_stats = languages[language]
        positive = language_stats[True]
        negative = language_stats[False]
        num_reviews = len(positive) + len(negative)
        ratio_num_reviews = len(positive) / num_reviews

        positive_length = sum(
            map(
                len,
                [review_dict['reviews'][review_id]['review'] for review_id in positive],
            ),
        )
        negative_length = sum(
            map(
                len,
                [review_dict['reviews'][review_id]['review'] for review_id in negative],
            ),
        )
        total_length = positive_length + negative_length
        ratio_length = positive_length / total_length

        print(
            'Language = {:10} #reviews = {:5} ({:.0%} positive) ; #characters = {:10} ({:.0%} positive)'.format(
                language.title(),
                num_reviews,
                ratio_num_reviews,
                total_length,
                ratio_length,
            ),
        )

    return


if __name__ == '__main__':
    review_dict = load_reviews()
    print_global_summary(review_dict)
    print_regional_summary(review_dict)
