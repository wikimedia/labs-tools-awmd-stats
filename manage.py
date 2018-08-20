#!/usr/bin/env python

# Author: Derick N. Alangi

import os

from flask_script import Manager

from awmdstats import create_app

# Run in particular environment
env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('awmdstats.settings.%sConfig' % env.capitalize())

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
