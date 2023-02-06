import steamreviews
import steamspypi


def get_artifact_app_id():
    # Store page: https://store.steampowered.com/app/583950/Artifact/

    artifact_app_id = 583950

    return artifact_app_id


def dowload_reviews(app_id=None):
    # For app_id, download all the reviews

    if app_id is None:
        app_id = get_artifact_app_id()

    review_dict, query_count = steamreviews.download_reviews_for_app_id(app_id)

    return review_dict


def load_reviews(app_id=None):
    if app_id is None:
        app_id = get_artifact_app_id()

    review_dict = steamreviews.load_review_dict(app_id)

    return review_dict


def download_reviews_for_top_100():
    # For each of the top 100 most played games, download English reviews, sorted by helpfulness, for the past 4 weeks

    data_request = {}
    data_request['request'] = 'top100in2weeks'
    data = steamspypi.download(data_request)

    app_ids = list(data.keys())

    request_params = {}
    request_params['language'] = 'english'
    request_params['filter'] = 'recent'
    request_params[
        'day_range'
    ] = '28'  # focus on reviews which were published during the past four weeks

    steamreviews.download_reviews_for_app_id_batch(
        app_ids,
        chosen_request_params=request_params,
    )

    return


def main():
    # Artifact
    review_dict = dowload_reviews()

    # Top 100
    download_reviews_for_top_100()

    return


if __name__ == '__main__':
    main()
