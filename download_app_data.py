import steampi.api
import steamspypi

from download_review_data import get_artifact_app_id


def download_app_details(app_id=None):
    # For app_id, download app details (including store description)

    if app_id is None:
        app_id = get_artifact_app_id()

    app_id = str(app_id)

    (app_details, _, _) = steampi.api.load_app_details(app_id)

    return app_details


def download_app_details_for_top_100():
    # For each of the top 100 most played games, download app details

    data_request = dict()
    data_request['request'] = 'top100in2weeks'
    data = steamspypi.download(data_request)

    app_ids = list(data.keys())

    for app_id in app_ids:
        (_, _, _) = steampi.api.load_app_details(app_id)

    return


def main():
    # Artifact
    review_dict = download_app_details()

    # Top 100
    download_app_details_for_top_100()

    return


if __name__ == '__main__':
    main()
