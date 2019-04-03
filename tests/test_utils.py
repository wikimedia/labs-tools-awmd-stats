#!/usr/bin/env python3

# Author: Derick N. Alangi
# Unit tests for utility functions in the application
# TODO: We intend to have 100% test coverage

import pytest
import time
import tinydb

from datetime import datetime

from awmdstats.utils import db_has_month
from awmdstats.utils import decrement_month, filter_month
from awmdstats.utils import increment_month, month_to_date
from awmdstats.utils import get_contributor_stats, get_contributors
from awmdstats.utils import get_current_month
from awmdstats.utils import get_db
from awmdstats.utils import get_doc_list
from awmdstats.utils import get_stats_from_db
from awmdstats.utils import read_contributors_from_file
from awmdstats.utils import patch_exists


@pytest.mark.usefixtures('testapp')
class TestUtils:
    """Test utility functions in the application."""

    # Test get_current_month() method
    def test_get_current_month(self, formatted='%Y-%m'):
        y_m_format = time.strftime(formatted)
        assert get_current_month(formatted) == y_m_format

    # Test db_has_month() method
    def test_db_has_month_with_data(self):
        status = db_has_month('2018-07')  # search month with data
        assert bool(status) is True  # returns True for month with data

    # Test db_has_month() method (with no data)
    # T219098: Use a far behind date as fix
    def test_db_has_month_without_data(self):
        #  Past month with no data
        #  https://tools.wmflabs.org/awmd-stats/month/1900-12.
        status = db_has_month('1900-12')  # search month without data
        assert bool(status) is False  # returns False for month without data

    # Test decrement_month() method
    def test_decrement_month(self):
        assert decrement_month('2018-08', 2) == '2018-06-01'

    # Test read_contributors_from_file() method
    def test_read_contributors_from_file(self):
        contributors = read_contributors_from_file()
        # returns False if isn't a list or is empty
        assert len(contributors) > 0 and isinstance(contributors, list)

    # Test get_contributors() method
    def test_get_contributors(self):
        month = '2018-07'
        stats = get_stats_from_db(month)
        contributors = get_contributors(stats, month)
        assert len(contributors) > 0 and isinstance(contributors, list)

    # Test get_contributor_stats() method
    def test_get_contributor_stats_with_data(self):
        stats = get_contributor_stats('Rosalieper', '2018-07')
        assert len(stats) > 0 and isinstance(stats, list)

    def test_get_contributor_stats_without_data(self):
        #  Past month with no data:
        #  https://tools.wmflabs.org/awmd-stats/contributor/Rosalieper/2018-04.
        stats = get_contributor_stats('BamLifa', '2018-04')
        assert len(stats) < 1 and isinstance(stats, list)

    # Test get_db() method
    def test_get_db(self):
        db = get_db()
        assert isinstance(db, tinydb.database.TinyDB)

    # Test get_doc_list() method
    def test_get_doc_list(self):
        doc_list = get_doc_list('awmdstats/templates/docs')
        assert len(doc_list) > 0 and isinstance(doc_list, list)

    # Test filter_month() method
    def test_filter_month(self):
        status = filter_month('2018-07-14', '2018-07')
        # returns True if month is found if full date time
        assert bool(status) is True

    # Test increment_month() method
    def test_increment_month(self):
        assert increment_month('2018-08', 2) == '2018-10-01'

    # Test month_to_date() method
    def test_month_to_date(self):
        assert month_to_date('2018-08') == datetime(2018, 8, 1)

    # Test get_stats_from_db() method
    def test_get_stats_from_db_with_data(self):
        # Test for existing stats
        stats = get_stats_from_db('2019-03')
        assert len(stats) > 0

    # Test get_stats_from_db_without_data() method
    def test_get_stats_from_db_without_data(self):
        # Test for non-existent stats
        stats = get_stats_from_db('2017-03')
        assert len(stats) < 1

    # Test patch_exists() method
    def test_patch_exists_with_data(self):
        # Test for existing patch
        patch = {'created': '2019-03-13 08:14:04.000000000',
                 'username': 'jeropbrenda'}
        status = patch_exists(patch)
        assert bool(status) is True

    # Test patch_exists() method (with no data)
    def test_patch_exists_without_data(self):
        # Test for non-existent patch
        patch = {'created': '2017-03-13 08:14:04.000000000',
                 'username': 'jeropbrenda'}
        status = patch_exists(patch)
        assert bool(status) is False
