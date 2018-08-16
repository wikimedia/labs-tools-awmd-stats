# Author: Derick N. Alangi
# Unit tests for the application
# TODO: We intend to have 100% test coverage

# Section 1: Test all routes
# Section 2: Test all UD methods

import unittest
from app import *

class AppTestCase(unittest.TestCase):
	""" Tests for the application. """

	###=== Section 1: Test all the routes===###
	def setUp(self):
		self.app = app.test_client()

	# Test the / (index) route response status_code
	def test_index(self):
		response = self.app.get('/')
		self.assertEquals(response.status_code, 200)

	# Test the /test route response status_code
	def test_test(self):
		response = self.app.get('/test')
		self.assertEquals(response.status_code, 200)

	# Test the /raw/ route response status_code
	def test_raw_route(self):
		response = self.app.get('/raw/')
		self.assertEquals(response.status_code, 200)

	# Test the /raw/<month> route response status_code
	def test_raw_month_route(self):
		response = self.app.get('/raw/2018-01')
		self.assertEquals(response.status_code, 200)

	# Test the /month/<month> route response status_code
	def test_month_route(self):
		response = self.app.get('/month/2018-01')
		self.assertEquals(response.status_code, 200)

	# Test the /contributor/<username>/<month>
	def test_contributor_username_month_route(self):
		response = self.app.get('/contributor/D3r1ck01/2018-02')
		self.assertEquals(response.status_code, 200)


	###=== Section 2: Test all the UD methods===###

	# Test getCurrentMonth() method
	def testGetCurrentMonth(self, formatted="%Y-%m"):
		Y_M_format = time.strftime(formatted)
		self.assertEquals(getCurrentMonth(formatted), Y_M_format)

	# Test dbHasMonth() method
	def testDbHasMonth_WithData(self):
		status = dbHasMonth("2018-02") # search month with data
		self.assertEquals(status, True) # returns True for month with data

	def testDbHasMonth_WithoutData(self):
		# Past month with no data: https://tools.wmflabs.org/awmd-stats/month/2017-11.
		status = dbHasMonth("2017-11") # search month without data
		self.assertEquals(status, False) # returns False for month without data

# Execute the unit tests
if __name__ == '__main__':
	unittest.main()
