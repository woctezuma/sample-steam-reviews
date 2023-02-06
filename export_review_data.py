from pathlib import Path

import steamspypi

from download_review_data import get_artifact_app_id
from filter_review_data import filter_reviews
from sort_review_data import get_useful_review_ids


def concatenate_reviews_as_a_large_text(english_review_dict, separator='\n'):
    useful_positive_review_ids = get_useful_review_ids(
        english_review_dict,
        voted_up=True,
    )
    useful_negative_review_ids = get_useful_review_ids(
        english_review_dict,
        voted_up=False,
    )

    # Concatenate lists of review ids
    sorted_review_ids = useful_positive_review_ids + useful_negative_review_ids

    # Concatenate lists of reviews
    review_list = [
        english_review_dict[review_id]['review'] for review_id in sorted_review_ids
    ]

    concatenated_reviews = separator.join(review_list)

    return concatenated_reviews


def get_output_folder_name():
    output_folder = 'output/'
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    return output_folder


def get_output_file_name(app_id=None):
    if app_id is None:
        app_id = get_artifact_app_id()

    file_extension = '.txt'
    language_file_name = get_output_folder_name() + str(app_id) + file_extension
    return language_file_name


def main():
    app_ids = [get_artifact_app_id()]

    data_request = dict()
    data_request['request'] = 'top100in2weeks'
    data = steamspypi.download(data_request)

    app_ids += list(data.keys())

    for app_id in app_ids:
        english_review_dict = filter_reviews(app_id)

        concatenated_reviews = concatenate_reviews_as_a_large_text(english_review_dict)

        with open(get_output_file_name(app_id), 'w', encoding='utf8') as f:
            print(concatenated_reviews, file=f)

    return


if __name__ == '__main__':
    main()
