#!/usr/bin/env python

# Author: Derick N. Alangi

import pytest

from awmdstats import create_app

@pytest.fixture()
def testapp(request):
    app = create_app('awmdstats.settings.TestConfig')
    client = app.test_client()

    return client
