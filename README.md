# Sample Steam Reviews

[![Build status][build-image]][build]
[![Updates][dependency-image]][pyup]
[![Python 3][python3-image]][pyup]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to sample Steam reviews for the games called [Artifact](https://store.steampowered.com/app/583950/Artifact/).


## Requirements

-   Install the latest version of [Python 3.X](https://www.python.org/downloads/).
-   Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Download Steam reviews for Artifact and for the top 100 most played games in the past 4 weeks

```
python download_review_data.py
```

### Extract English reviews

```
python filter_review_data.py
```

### Display info about reviews

```
python display_review_data.py
```


### Download app details for Artifact and for the top 100 most played games in the past 4 weeks

```
python download_app_data.py
```


## Results

TODO

## References

TODO


[build]: <https://travis-ci.org/woctezuma/sample-steam-reviews>
[build-image]: <https://travis-ci.org/woctezuma/sample-steam-reviews.svg?branch=master>

[pyup]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/python-3-shield.svg>

[codecov]: <https://codecov.io/gh/woctezuma/sample-steam-reviews>
[codecov-image]: <https://codecov.io/gh/woctezuma/sample-steam-reviews/branch/master/graph/badge.svg>

[codacy]: <https://www.codacy.com/app/woctezuma/sample-steam-reviews>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/1f8b420b27344e48bfa54dee59d76f62>

