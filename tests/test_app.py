#!/usr/bin/env python

# Author: Derick N. Alangi
# Unit tests for the application
# TODO: We intend to have 100% test coverage

# Section 1: Test all routes
# Section 2: Test all UD methods

import pytest
import time
from awmdstats.utils import dbHasMonth
from awmdstats.utils import getCurrentMonth

@pytest.mark.usefixtures("testapp")
class TestApp:
	""" Tests for the application. """

	###=== Section 1: Test all the routes===###

	# Test the / (index) route response status_code
	def test_index_route(self, testapp):
		response = testapp.get('/')
		assert response.status_code == 200

	# Test the /test route response status_code
	def test_test_route(self, testapp):
		response = testapp.get('/test')
		assert response.status_code == 200

	# Test the /raw/ route response status_code
	def test_raw_route(self, testapp):
		response = testapp.get('/raw/')
		assert response.status_code == 200

	# Test the /raw/<month> route response status_code
	def test_raw_month_route(self, testapp):
		response = testapp.get('/raw/2018-01')
		assert response.status_code == 200

	# Test the /month/<month> route response status_code
	def test_month_month_route(self, testapp):
		response = testapp.get('/month/2018-01')
		assert response.status_code == 200

	# Test the /contributor/<username>/<month>
	def test_contributor_username_month_route(self, testapp):
		response = testapp.get('/contributor/D3r1ck01/2018-07')
		assert response.status_code == 200

	# Test the /refresh/ route response status_code
	def test_refresh_route(self, testapp):
		response = testapp.get('/refresh/')
		assert response.status_code == 200

	# Test the /refresh/<month> route response status_code
	def test_refresh_month_route(self, testapp):
		response = testapp.get('/refresh/2018-01')
		assert response.status_code == 200


	###=== Section 2: Test all the UD methods===###

	# Test getCurrentMonth() method
	def testGetCurrentMonth(self, formatted="%Y-%m"):
		Y_M_format = time.strftime(formatted)
		assert getCurrentMonth(formatted) == Y_M_format

	# Test dbHasMonth() method
	def testDbHasMonth_WithData(self):
		status = dbHasMonth("2018-07") # search month with data
		assert status == True # returns True for month with data

	def testDbHasMonth_WithoutData(self):
		# Past month with no data: https://tools.wmflabs.org/awmd-stats/month/2017-11.
		status = dbHasMonth("2017-11") # search month without data
		assert status == False # returns False for month without data
