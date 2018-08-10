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

## Quickstart the app
```bash
export FLASK_APP=app.py
flask run
```

# Track your contributions

* You want your contributions to be tracked by this tool? Nicely add your information in the `contributors.json` in the `JSON` format and the tool will automatically run a cron to fetch your contributions.


# Contributors

* [Samuel Guébo](https://github.com/samuelguebo) - Project Lead
* [Derick Alangi](https://github.com/ch3nkula) - Supporter