#!/usr/bin/env python3

# Author: Derick N. Alangi

from flask_script import Manager

from awmdstats.app import create_app

app = create_app()

manager = Manager(app)


@manager.command
def debug_mode():
    """
    Enable running the app in debug mode.

    This allows the app context to be reloaded upon changes and save at
    run time.
    """
    app.run(debug=True)


if __name__ == '__main__':
    manager.run()
