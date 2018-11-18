#!/usr/bin/env python3

# Author: Derick N. Alangi
# Unit tests for utility functions in the application
# TODO: We intend to have 100% test coverage

import pytest
import time
import tinydb

from datetime import datetime

from awmdstats.utils import dbHasMonth
from awmdstats.utils import decrementMonth, filterMonth, incrementMonth, monthToDate
from awmdstats.utils import getContributorStats
from awmdstats.utils import getCurrentMonth
from awmdstats.utils import getDb
from awmdstats.utils import readContributorsFromFile


@pytest.mark.usefixtures('testapp')
class TestUtils:
    """Test utility functions in the application."""

    #  Test getCurrentMonth() method
    def testGetCurrentMonth(self, formatted='%Y-%m'):
        Y_M_format = time.strftime(formatted)
        assert getCurrentMonth(formatted) == Y_M_format

    #  Test dbHasMonth() method
    def testDbHasMonth_WithData(self):
        status = dbHasMonth('2018-07')  # search month with data
        assert bool(status) is True  # returns True for month with data

    def testDbHasMonth_WithoutData(self):
        #  Past month with no data: https://tools.wmflabs.org/awmd-stats/month/2017-11.
        status = dbHasMonth('2017-11')  # search month without data
        assert bool(status) is False  # returns False for month without data

    # Test decrementMonth() method
    def testDecrementMonth(self):
        assert decrementMonth('2018-08', 2) == '2018-06-01'

    # Test readContributorsFromFile() method
    def testReadContributorsFromFile(self):
        contributors = readContributorsFromFile()
        # returns False if isn't a list or is empty
        assert len(contributors) > 0 and isinstance(contributors, list)

    # Test getContributorStats() method
    def testGetContributorStats_WithData(self):
        stats = getContributorStats('Rosalieper', '2018-07')
        assert len(stats) > 0 and isinstance(stats, list)

    def testGetContributorStats_WithoutData(self):
        #  Past month with no data:
        #  https://tools.wmflabs.org/awmd-stats/contributor/Rosalieper/2018-04.
        stats = getContributorStats('BamLifa', '2018-04')
        assert len(stats) < 1 and isinstance(stats, list)

    # Test getDb() method
    def testGetDb(self):
        db = getDb()
        assert isinstance(db, tinydb.database.TinyDB)

    # Test filterMonth() method
    def testFilterMonth(self):
        status = filterMonth('2018-07-14', '2018-07')
        # returns True if month is found if full date time
        assert bool(status) is True

    # Test incrementMonth() method
    def testIncrementMonth(self):
        assert incrementMonth('2018-08', 2) == '2018-10-01'

    # Test monthToDate() method
    def testMonthToDate(self):
        assert monthToDate('2018-08') == datetime(2018, 8, 1)
