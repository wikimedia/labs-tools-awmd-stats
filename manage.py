#!/usr/bin/env python3

# Author: Derick N. Alangi

import os

from flask_script import Manager

from awmdstats.app import create_app

# Run in particular environment
env = os.environ.get('APPNAME_ENV', 'dev')  # WIP
app = create_app('awmdstats.settings.%sConfig' % env.capitalize())

manager = Manager(app)


@manager.command
def debug_mode():
    """
    Enable running the app in debug mode.

    This allows the app context to be reloaded upon changes and save at
    run time. Use "python manage.py debug_mode" for this feature.
    """
    app.run(debug=True)


if __name__ == '__main__':
    manager.run()
