#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Derick N. Alangi

import pytest

from awmdstats.app import create_app


@pytest.fixture()
def testapp():
    app = create_app()
    client = app.test_client()

    return client
