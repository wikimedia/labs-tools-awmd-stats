# awmd-stats

Africa Wikimedia Developer (AWMD) statisitics tool is meant for gathering monthly statistics of African technical contributors into Wikimedia projects such as; MediaWiki, MediaWiki extensions, etc. For more information see: https://www.mediawiki.org/wiki/Awmd-stats

## Ranking method
The tool uses a method to rank different contributors based on their patches and the state of the patch.
Assume "m" is the number of patches merged and "n" is the number of patches under review, the formula is:
```
points = (2 x m) + n
```

# Requirements

* [Python 3.x+](https://www.python.org/downloads/)
* [PIP (Python Dependency Manager)](https://pip.pypa.io/en/stable/installing/)

## Clone project
```bash
git clone ssh://<USERNAME>@gerrit.wikimedia.org:29418/labs/tools/awmd-stats
```

## Setup and documentation

Install application dependencies and regenerate documentation using the `setup.sh` script:
```bash
./setup.sh
```
The above script attempts to check system requirements and tell informs user on next steps.

## Quickstart the tool
```bash
export FLASK_APP=flasky.py
flask run
```

## Read the code documentations
To view documentation of the codes which makes use of the docstrings, use this endpoint
#### On localhost
```bash
localhost:5000/docs/index
```

#### On Toolforge server
```bash
https://tools.wmflabs.org/awmd-stats/docs/index
```

## Testing the tool
```bash
pip install pytest
```

Then run the command below (make sure you're in the project's root for example):
```bash
py.test -v tests/
```

`NOTE`: If you find any failing test, report on Phabricator here: https://phabricator.wikimedia.org/project/board/2858/.

## Coding conventions
The contributors to this tool are strongly encouraged to use the following coding guidelines:

* [MediaWiki's coding conventions for JavaScript](https://www.mediawiki.org/wiki/Manual:Coding_conventions/JavaScript)
* [MediaWiki's manual for Pywikibot/Gerrit developers](https://www.mediawiki.org/wiki/Manual:Pywikibot/Development/Guidelines#Making_a_patch)


# Track your contributions

* You want your contributions to be tracked by this tool? Nicely add your information in the `contributors.json` in the `JSON` format and the tool will automatically run a cron to fetch your contributions.


# Contributors

* [Samuel Guébo](https://github.com/samuelguebo) - Project Lead
* [Derick Alangi](https://github.com/xSavitar) - Contributor
