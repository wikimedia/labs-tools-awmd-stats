# awmd-stats

Africa Wikimedia Developer (AWMD) Tool for gathering monthly statistics of African technical contributors into Wikimedia projects e.g. MediaWiki, MediaWiki extensions, etc.


# Requirements

* [Python 3.x+](https://www.python.org/downloads/)
* [PIP (Python Dependency Manager)](https://pip.pypa.io/en/stable/installing/)

## Installing dependencies

Install application dependencies using the `install-deps.sh` script:
```bash
./install-deps.sh
```
The above script attempts to check system requirements and tell informs user on next steps.

## Quickstart the tool
```bash
python manage.py runserver
```

## Testing the tool
```bash
pip install pytest
```

Then run the command below (make sure you're in the project's root for example):
```
bash
py.test -v tests/
```

`NOTE`: If you find any failing test, report on Phabricator here: https://phabricator.wikimedia.org/project/board/2858/.

# Track your contributions

* You want your contributions to be tracked by this tool? Nicely add your information in the `contributors.json` in the `JSON` format and the tool will automatically run a cron to fetch your contributions.


# Contributors

* [Samuel Guébo](https://github.com/samuelguebo) - Project Lead
* [Derick Alangi](https://github.com/ch3nkula) - Contributor
