#!/usr/bin/env python3

# Author: Derick N. Alangi

import pytest

from awmdstats.app import create_app


@pytest.fixture()
def testapp(request):
    app = create_app('awmdstats.settings.TestConfig')
    client = app.test_client()

    return client
