#!/usr/bin/env python

# Author: Derick N. Alangi
# Unit tests for utility functions in the application
# TODO: We intend to have 100% test coverage

import pytest
import time

from awmdstats.utils import dbHasMonth
from awmdstats.utils import getCurrentMonth


@pytest.mark.usefixtures("testapp")
class TestUtils:
    """Test utility functions in the application."""

    #  Test getCurrentMonth() method
    def testGetCurrentMonth(self, formatted="%Y-%m"):
        Y_M_format = time.strftime(formatted)
        assert getCurrentMonth(formatted) == Y_M_format

    #  Test dbHasMonth() method
    def testDbHasMonth_WithData(self):
        status = dbHasMonth("2018-07")  # search month with data
        assert bool(status) is True  # returns True for month with data

    def testDbHasMonth_WithoutData(self):
        #  Past month with no data: https://tools.wmflabs.org/awmd-stats/month/2017-11.
        status = dbHasMonth("2017-11")  # search month without data
        assert bool(status) is False  # returns False for month without data
