import steamreviews


def get_artifact_app_id():
    # Store page: https://store.steampowered.com/app/583950/Artifact/

    artifact_app_id = 583950

    return artifact_app_id


def dowload_reviews(app_id=None):
    if app_id is None:
        app_id = get_artifact_app_id()

    review_dict, query_count = steamreviews.download_reviews_for_app_id(app_id)

    return review_dict


def load_reviews(app_id=None):
    if app_id is None:
        app_id = get_artifact_app_id()

    review_dict = steamreviews.load_review_dict(app_id)

    return review_dict


if __name__ == '__main__':
    review_dict = dowload_reviews()
