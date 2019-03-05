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

### Download Steam reviews for Artifact

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

## Results

TODO

## References

TODO


[build]: <https://travis-ci.org/woctezuma/sample-steam-banners>
[build-image]: <https://travis-ci.org/woctezuma/sample-steam-banners.svg?branch=master>

[pyup]: <https://pyup.io/repos/github/woctezuma/sample-steam-banners/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/sample-steam-banners/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/sample-steam-banners/python-3-shield.svg>

[codecov]: <https://codecov.io/gh/woctezuma/sample-steam-banners>
[codecov-image]: <https://codecov.io/gh/woctezuma/sample-steam-banners/branch/master/graph/badge.svg>

[codacy]: <https://www.codacy.com/app/woctezuma/sample-steam-banners>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/TODO>

